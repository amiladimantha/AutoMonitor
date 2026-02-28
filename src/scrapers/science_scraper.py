"""Science news scraper"""
from typing import List, Dict
from src.scrapers.base_scraper import BaseScraper
from src.config.settings import Settings
import logging

logger = logging.getLogger(__name__)


class ScienceScraper(BaseScraper):
    """Scraper for science news and breakthroughs"""
    
    def __init__(self):
        settings = Settings()
        super().__init__(sources=settings.SCIENCE_NEWS_SOURCES)
        self.category = "Science"
    
    def scrape(self) -> List[Dict]:
        """Scrape science news from multiple sources"""
        all_articles = []
        
        for source in self.sources:
            try:
                logger.info(f"Scraping science news from {source}")
                articles = self.extract_articles_from_feed(source)
                all_articles.extend(articles)
            except Exception as e:
                logger.error(f"Error scraping science news from {source}: {str(e)}")
        
        # Remove duplicates and limit results
        unique_articles = {article['url']: article 
                          for article in all_articles}.values()
        
        return list(unique_articles)[:self.settings.MAX_ARTICLES_PER_CATEGORY]
