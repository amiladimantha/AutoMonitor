"""
LLM-powered article deduplication and merging.

Strategy
--------
1. If OPENAI_API_KEY is set and ENABLE_LLM_DEDUP is true, send a compact
   batch of article titles/descriptions to GPT and ask it to return JSON
   groupings of articles that cover the same underlying story.
2. Otherwise (no API key or openai package not installed) fall back to a
   purely local fuzzy-title similarity check using difflib.

In both cases, articles within the same group are merged into a single
"digest" dict so only one Telegram message is sent per story.
"""

import json
import logging
from difflib import SequenceMatcher
from typing import List, Dict, Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

# Optional LLM dependency — only required when ENABLE_LLM_DEDUP=true
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # type: ignore


def _title_similarity(a: str, b: str) -> float:
    """Return a 0-1 similarity score between two title strings."""
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()


def _hostname(url: str) -> str:
    """Return a clean hostname from a URL, e.g. 'arstechnica.com'."""
    try:
        return urlparse(url).netloc.replace("www.", "").strip()
    except Exception:
        return ""


class ArticleDeduplicator:
    """
    Groups semantically similar articles and merges each group into a
    single 'digest' article dict before messages are sent to Telegram.
    """

    def __init__(self, settings):
        self.settings = settings
        self._openai_client = None

        if getattr(settings, "ENABLE_LLM_DEDUP", False) and getattr(settings, "OPENAI_API_KEY", ""):
            if OpenAI is None:
                logger.warning(
                    "openai package not installed – falling back to fuzzy dedup. "
                    "Run: pip install openai"
                )
            else:
                try:
                    self._openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
                    logger.info(
                        f"LLM deduplicator ready (model: {settings.LLM_DEDUP_MODEL})"
                    )
                except Exception as e:
                    logger.warning(f"Failed to init OpenAI client: {e}")
        else:
            logger.info("LLM dedup disabled or no API key – using fuzzy title dedup")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def deduplicate(self, articles: List[Dict]) -> List[Dict]:
        """
        Return a deduplicated list.  Articles covering the same story are
        merged into one digest entry with combined metadata.
        """
        if len(articles) <= 1:
            return articles

        if self._openai_client:
            return self._llm_deduplicate(articles)
        return self._fuzzy_deduplicate(articles)

    # ------------------------------------------------------------------
    # LLM path
    # ------------------------------------------------------------------

    def _llm_deduplicate(self, articles: List[Dict]) -> List[Dict]:
        """Ask the LLM to group articles that cover the same event/story."""
        items = [
            {
                "id": i,
                "title": a.get("title", ""),
                "summary": (a.get("description") or "")[:200],
            }
            for i, a in enumerate(articles)
        ]

        prompt = (
            "You are a news deduplication assistant.\n"
            "Group the following news articles so that articles covering the "
            "SAME underlying story or event are in the same group, even if "
            "they come from different sources or are worded differently.\n"
            "Return ONLY a valid JSON array of groups, where each group is an "
            "array of article IDs. Every article ID must appear exactly once.\n\n"
            f"Articles:\n{json.dumps(items, ensure_ascii=False)}\n\n"
            "Example output: [[0,2],[1],[3,4,5]]"
        )

        try:
            response = self._openai_client.chat.completions.create(
                model=self.settings.LLM_DEDUP_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=400,
            )
            raw = response.choices[0].message.content.strip()
            # Strip markdown code fences if the model wraps its response
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            groups: List[List[int]] = json.loads(raw.strip())

            # Validate: every index 0..n-1 appears exactly once
            seen = set()
            for g in groups:
                for idx in g:
                    seen.add(idx)
            if seen != set(range(len(articles))):
                raise ValueError("LLM returned incomplete grouping")

            logger.info(
                f"LLM grouped {len(articles)} articles → {len(groups)} digest(s)"
            )
            return self._merge_groups(articles, groups)

        except Exception as exc:
            logger.warning(f"LLM dedup failed ({exc}); falling back to fuzzy dedup")
            return self._fuzzy_deduplicate(articles)

    # ------------------------------------------------------------------
    # Fuzzy fallback path
    # ------------------------------------------------------------------

    def _fuzzy_deduplicate(self, articles: List[Dict]) -> List[Dict]:
        """
        Group articles whose titles are above DEDUP_SIMILARITY_THRESHOLD
        using a greedy single-linkage approach.
        """
        threshold: float = getattr(self.settings, "DEDUP_SIMILARITY_THRESHOLD", 0.6)
        used = [False] * len(articles)
        groups: List[List[int]] = []

        for i in range(len(articles)):
            if used[i]:
                continue
            group = [i]
            used[i] = True
            for j in range(i + 1, len(articles)):
                if not used[j]:
                    sim = _title_similarity(
                        articles[i].get("title", ""),
                        articles[j].get("title", ""),
                    )
                    if sim >= threshold:
                        group.append(j)
                        used[j] = True
            groups.append(group)

        duplicates_found = sum(1 for g in groups if len(g) > 1)
        if duplicates_found:
            logger.info(
                f"Fuzzy dedup: {len(articles)} articles → "
                f"{len(groups)} digest(s) ({duplicates_found} merge(s))"
            )
        return self._merge_groups(articles, groups)

    # ------------------------------------------------------------------
    # Merging logic (shared by both paths)
    # ------------------------------------------------------------------

    def _merge_groups(
        self, articles: List[Dict], groups: List[List[int]]
    ) -> List[Dict]:
        """
        For singleton groups return the article unchanged.
        For multi-article groups return a single merged 'digest' dict.
        """
        result: List[Dict] = []

        for group in groups:
            if len(group) == 1:
                result.append(articles[group[0]])
                continue

            members = [articles[i] for i in group]
            primary = members[0]  # use first article as the base

            # Collect unique hostnames as source attribution
            sources = []
            all_urls = []
            for m in members:
                url = m.get("url", "")
                if url:
                    all_urls.append(url)
                    host = _hostname(url)
                    if host and host not in sources:
                        sources.append(host)

            # Use the longest description as the body
            best_desc = max(
                (m.get("description") or "" for m in members), key=len
            )

            merged: Dict = {
                **primary,
                # Keep primary title (usually the freshest / most informative)
                "title": primary.get("title", ""),
                "description": best_desc,
                # Overwrite author with source list so the reader knows it's
                # a digest and which outlets covered it
                "author": ", ".join(sources) if sources else primary.get("author", ""),
                # Extra fields consumed by TelegramClient._format_article
                "merged_urls": all_urls,
                "source_count": len(members),
            }
            result.append(merged)

        return result
