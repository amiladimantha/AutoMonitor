"""Test suite for AutoMonitor"""
import unittest
from unittest.mock import patch, MagicMock
from src.scrapers.tech_scraper import TechScraper
from src.scrapers.science_scraper import ScienceScraper
from src.scrapers.ai_scraper import AIScraper
from src.scrapers.military_scraper import MilitaryScraper
from src.config.settings import Settings
from src.utils.deduplicator import ArticleDeduplicator, _title_similarity


class TestSettings(unittest.TestCase):
    """Test Settings configuration"""

    def test_settings_load(self):
        """Test that settings load correctly"""
        settings = Settings()
        self.assertIsNotNone(settings.LOG_LEVEL)
        self.assertIsNotNone(settings.TELEGRAM_BOT_TOKEN)

    def test_scrape_interval(self):
        """Test scrape interval is positive"""
        settings = Settings()
        self.assertGreater(settings.SCRAPE_INTERVAL, 0)

    def test_source_lists_non_empty(self):
        """Each category must have at least one RSS URL configured"""
        s = Settings()
        self.assertTrue(len(s.TECH_NEWS_SOURCES) > 0)
        self.assertTrue(len(s.SCIENCE_NEWS_SOURCES) > 0)
        self.assertTrue(len(s.AI_NEWS_SOURCES) > 0)
        self.assertTrue(len(s.MILITARY_NEWS_SOURCES) > 0)

    def test_dedup_settings_present(self):
        """LLM dedup settings must be present with sane defaults"""
        s = Settings()
        self.assertIsInstance(s.ENABLE_LLM_DEDUP, bool)
        self.assertIsInstance(s.LLM_DEDUP_MODEL, str)
        self.assertGreater(s.DEDUP_SIMILARITY_THRESHOLD, 0)
        self.assertLessEqual(s.DEDUP_SIMILARITY_THRESHOLD, 1)


# ---------------------------------------------------------------------------
# Deduplicator tests
# ---------------------------------------------------------------------------

class TestTitleSimilarity(unittest.TestCase):
    """Unit tests for the title similarity helper"""

    def test_identical_titles(self):
        self.assertEqual(_title_similarity("foo bar", "foo bar"), 1.0)

    def test_completely_different(self):
        self.assertLess(_title_similarity("apple pie", "quantum physics"), 0.4)

    def test_case_insensitive(self):
        self.assertEqual(
            _title_similarity("OpenAI Releases GPT-5", "openai releases gpt-5"), 1.0
        )

    def test_paraphrase_is_high(self):
        # Same story, slightly different wording
        score = _title_similarity(
            "OpenAI launches GPT-5 model",
            "OpenAI releases its new GPT-5 model",
        )
        self.assertGreater(score, 0.55)


class TestFuzzyDeduplicator(unittest.TestCase):
    """Tests for ArticleDeduplicator using the local fuzzy path (no OpenAI key)"""

    def _make_settings(self, threshold=0.6):
        s = Settings()
        s.ENABLE_LLM_DEDUP = False  # force fuzzy path
        s.OPENAI_API_KEY = ""
        s.DEDUP_SIMILARITY_THRESHOLD = threshold
        return s

    def test_no_articles_returns_empty(self):
        dedup = ArticleDeduplicator(self._make_settings())
        self.assertEqual(dedup.deduplicate([]), [])

    def test_single_article_unchanged(self):
        articles = [{'title': 'Only article', 'url': 'https://a.com/1', 'description': ''}]
        dedup = ArticleDeduplicator(self._make_settings())
        result = dedup.deduplicate(articles)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['url'], 'https://a.com/1')

    def test_unique_articles_all_kept(self):
        articles = [
            {'title': 'Quantum breakthrough at CERN', 'url': 'https://a.com/1', 'description': ''},
            {'title': 'New iPhone 17 hands-on review', 'url': 'https://b.com/2', 'description': ''},
            {'title': 'Mars mission launch date confirmed', 'url': 'https://c.com/3', 'description': ''},
        ]
        dedup = ArticleDeduplicator(self._make_settings())
        result = dedup.deduplicate(articles)
        self.assertEqual(len(result), 3)

    def test_duplicate_titles_merged_into_one(self):
        articles = [
            {'title': 'OpenAI releases GPT-5 model', 'url': 'https://techcrunch.com/gpt5', 'description': 'Big news'},
            {'title': 'OpenAI releases GPT-5 model', 'url': 'https://theverge.com/gpt5',  'description': 'OpenAI has released GPT-5'},
            {'title': 'Mars rover finds water ice',  'url': 'https://nasa.gov/mars',       'description': 'NASA news'},
        ]
        dedup = ArticleDeduplicator(self._make_settings(threshold=0.6))
        result = dedup.deduplicate(articles)
        # Two duplicate GPT-5 articles should collapse into one digest
        self.assertEqual(len(result), 2)

    def test_merged_article_has_digest_fields(self):
        articles = [
            {'title': 'AI chip race heats up', 'url': 'https://ars.com/1', 'description': 'Short'},
            {'title': 'AI chip race heats up', 'url': 'https://verge.com/1', 'description': 'Much longer description here'},
        ]
        dedup = ArticleDeduplicator(self._make_settings(threshold=0.95))
        result = dedup.deduplicate(articles)
        self.assertEqual(len(result), 1)
        digest = result[0]
        self.assertEqual(digest['source_count'], 2)
        self.assertIn('merged_urls', digest)
        self.assertEqual(len(digest['merged_urls']), 2)
        # Should pick the longest description
        self.assertEqual(digest['description'], 'Much longer description here')

    def test_all_urls_tracked_in_merged_urls(self):
        articles = [
            {'title': 'Same story', 'url': 'https://site1.com/x', 'description': ''},
            {'title': 'Same story', 'url': 'https://site2.com/x', 'description': ''},
            {'title': 'Same story', 'url': 'https://site3.com/x', 'description': ''},
        ]
        dedup = ArticleDeduplicator(self._make_settings(threshold=0.99))
        result = dedup.deduplicate(articles)
        self.assertEqual(len(result), 1)
        self.assertCountEqual(
            result[0]['merged_urls'],
            ['https://site1.com/x', 'https://site2.com/x', 'https://site3.com/x'],
        )


class TestLLMDeduplicator(unittest.TestCase):
    """Tests for the LLM path using a mocked OpenAI client"""

    def _make_settings_with_key(self):
        s = Settings()
        s.ENABLE_LLM_DEDUP = True
        s.OPENAI_API_KEY = 'sk-test-fake-key'
        s.LLM_DEDUP_MODEL = 'gpt-4o-mini'
        s.DEDUP_SIMILARITY_THRESHOLD = 0.6
        return s

    @patch('src.utils.deduplicator.OpenAI')
    def test_llm_groups_articles(self, mock_openai_cls):
        """LLM response grouping [[0,1],[2]] → 2 results"""
        import json
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content='[[0,1],[2]]'))]
        )

        dedup = ArticleDeduplicator(self._make_settings_with_key())
        articles = [
            {'title': 'GPT-5 launch', 'url': 'https://a.com/1', 'description': 'x'},
            {'title': 'OpenAI unveils GPT-5', 'url': 'https://b.com/2', 'description': 'y'},
            {'title': 'Mars water confirmed', 'url': 'https://c.com/3', 'description': 'z'},
        ]
        result = dedup.deduplicate(articles)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['source_count'], 2)

    @patch('src.utils.deduplicator.OpenAI')
    def test_llm_fallback_on_bad_json(self, mock_openai_cls):
        """If LLM returns garbage JSON, fall back to fuzzy dedup without crashing"""
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content='not valid json at all'))]
        )

        dedup = ArticleDeduplicator(self._make_settings_with_key())
        articles = [
            {'title': 'NASA confirms water ice on Mars surface', 'url': 'https://a.com/1', 'description': ''},
            {'title': 'New iPhone 17 hands-on review', 'url': 'https://b.com/2', 'description': ''},
        ]
        # Should not raise — falls back to fuzzy; titles are distinct so both kept
        result = dedup.deduplicate(articles)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)  # both unique titles → kept separate


class TestTechScraper(unittest.TestCase):
    """Test Technology news scraper"""
    
    @patch('src.scrapers.tech_scraper.TechScraper.extract_articles_from_feed')
    def test_scrape_returns_list(self, mock_extract):
        """Test that scraper returns a list"""
        mock_extract.return_value = [
            {
                'title': 'Test Article',
                'url': 'https://example.com',
                'description': 'Test description'
            }
        ]
        
        scraper = TechScraper()
        articles = scraper.scrape()
        
        self.assertIsInstance(articles, list)


class TestScienceScraper(unittest.TestCase):
    """Test Science news scraper"""
    
    @patch('src.scrapers.science_scraper.ScienceScraper.extract_articles_from_feed')
    def test_scrape_returns_list(self, mock_extract):
        """Test that scraper returns a list"""
        mock_extract.return_value = []
        
        scraper = ScienceScraper()
        articles = scraper.scrape()
        
        self.assertIsInstance(articles, list)


class TestAIScraper(unittest.TestCase):
    """Test AI news scraper"""
    
    @patch('src.scrapers.ai_scraper.AIScraper.extract_articles_from_feed')
    def test_scrape_returns_list(self, mock_extract):
        """Test that scraper returns a list"""
        mock_extract.return_value = []
        
        scraper = AIScraper()
        articles = scraper.scrape()
        
        self.assertIsInstance(articles, list)


class TestMilitaryScraper(unittest.TestCase):
    """Test Military news scraper"""
    
    @patch('src.scrapers.military_scraper.MilitaryScraper.extract_articles_from_feed')
    def test_scrape_returns_list(self, mock_extract):
        """Test that scraper returns a list"""
        mock_extract.return_value = []
        
        scraper = MilitaryScraper()
        articles = scraper.scrape()
        
        self.assertIsInstance(articles, list)


if __name__ == '__main__':
    unittest.main()
