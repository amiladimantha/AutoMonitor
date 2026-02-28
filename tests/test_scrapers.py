"""Test suite for AutoMonitor"""
import unittest
from unittest.mock import patch, MagicMock
from src.scrapers.tech_scraper import TechScraper
from src.scrapers.science_scraper import ScienceScraper
from src.scrapers.ai_scraper import AIScraper
from src.scrapers.military_scraper import MilitaryScraper
from src.config.settings import Settings


class TestSettings(unittest.TestCase):
    """Test Settings configuration"""
    
    def test_settings_load(self):
        """Test that settings load correctly"""
        settings = Settings()
        self.assertIsNotNone(settings.TWILIO_ACCOUNT_SID)
        self.assertIsNotNone(settings.LOG_LEVEL)
    
    def test_scrape_interval(self):
        """Test scrape interval is positive"""
        settings = Settings()
        self.assertGreater(settings.SCRAPE_INTERVAL, 0)


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
