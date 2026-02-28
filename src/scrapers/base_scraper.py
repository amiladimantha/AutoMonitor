"""Base scraper class for all news scrapers"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import re
import requests
from bs4 import BeautifulSoup
import logging
from src.config.settings import Settings

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Abstract base class for all news scrapers"""
    
    def __init__(self, sources: List[str] = None):
        self.settings = Settings()
        self.sources = sources or []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def fetch_page(self, url: str) -> BeautifulSoup:
        """Fetch and parse a web page"""
        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.settings.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            raise
    
    def _clean_html(self, raw: str) -> str:
        """Strip HTML tags and clean up whitespace from text"""
        if not raw:
            return ''
        text = BeautifulSoup(raw, 'html.parser').get_text(separator=' ')
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _extract_image(self, entry) -> Optional[str]:
        """Try to extract an image URL from a feed entry"""
        # 1. media:content
        media = getattr(entry, 'media_content', None)
        if media and isinstance(media, list):
            for m in media:
                url = m.get('url', '')
                if url and any(url.lower().endswith(ext) for ext in ('.jpg', '.jpeg', '.png', '.webp', '.gif')):
                    return url
        
        # 2. media:thumbnail
        thumb = getattr(entry, 'media_thumbnail', None)
        if thumb and isinstance(thumb, list) and thumb[0].get('url'):
            return thumb[0]['url']
        
        # 3. enclosures
        for enc in getattr(entry, 'enclosures', []):
            if enc.get('type', '').startswith('image/'):
                return enc.get('href', '') or enc.get('url', '')
        
        # 4. Scan links
        for link in getattr(entry, 'links', []):
            if link.get('type', '').startswith('image/'):
                return link.get('href', '')
        
        # 5. Scan summary HTML for <img> tags
        summary_html = entry.get('summary', '') or entry.get('content', [{'value': ''}])[0].get('value', '')
        if summary_html:
            soup = BeautifulSoup(summary_html, 'html.parser')
            img = soup.find('img')
            if img and img.get('src'):
                src = img['src']
                if src.startswith('http'):
                    return src
        
        return None
    
    def extract_articles_from_feed(self, feed_url: str) -> List[Dict]:
        """Extract articles with rich data from RSS/XML feed"""
        import feedparser
        try:
            feed = feedparser.parse(feed_url)
            articles = []
            
            for entry in feed.entries[:self.settings.MAX_ARTICLES_PER_CATEGORY]:
                # Get and clean full description (up to 500 chars)
                raw_summary = entry.get('summary', '') or ''
                if not raw_summary:
                    content_list = entry.get('content', [])
                    raw_summary = content_list[0].get('value', '') if content_list else ''
                
                description = self._clean_html(raw_summary)
                # Trim to ~450 chars, ending on a full sentence if possible
                if len(description) > 450:
                    cutoff = description.rfind('.', 200, 450)
                    description = description[:cutoff + 1] if cutoff > 0 else description[:450] + '...'
                
                article = {
                    'title': self._clean_html(entry.get('title', '')),
                    'url': entry.get('link', ''),
                    'description': description,
                    'image': self._extract_image(entry),
                    'author': entry.get('author', '') or entry.get('author_detail', {}).get('name', ''),
                    'published': entry.get('published', '')
                }
                
                if article['title'] and article['url']:
                    articles.append(article)
            
            return articles
        
        except Exception as e:
            logger.error(f"Error parsing feed {feed_url}: {str(e)}")
            return []
    
    @abstractmethod
    def scrape(self) -> List[Dict]:
        """Scrape news articles - to be implemented by subclasses"""
        pass
