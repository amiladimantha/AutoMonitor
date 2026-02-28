"""Technology news scraper"""
from typing import List, Dict
from src.scrapers.base_scraper import BaseScraper
from src.config.settings import Settings
import logging

logger = logging.getLogger(__name__)


class TechScraper(BaseScraper):
    """Scraper for technology news"""
    
    def __init__(self):
        settings = Settings()
        super().__init__(sources=settings.TECH_NEWS_SOURCES)
        self.category = "Technology"
    
    def scrape(self) -> List[Dict]:
        """Scrape technology news from multiple sources"""
        all_articles = []
        
        for source in self.sources:
            try:
                logger.info(f"Scraping tech news from {source}")
                articles = self.extract_articles_from_feed(source)
                all_articles.extend(articles)
            except Exception as e:
                logger.error(f"Error scraping tech news from {source}: {str(e)}")
        
        # Remove duplicates and limit results
        unique_articles = {article['url']: article 
                          for article in all_articles}.values()
        
        return list(unique_articles)[:self.settings.MAX_ARTICLES_PER_CATEGORY]
