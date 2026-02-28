"""
AutoMonitor - Main Application Entry Point
"""
import json
import logging
import schedule
import time
from collections import deque
from pathlib import Path
from typing import Dict, Deque
from src.config.settings import Settings
from src.scrapers.tech_scraper import TechScraper
from src.scrapers.science_scraper import ScienceScraper
from src.scrapers.ai_scraper import AIScraper
from src.scrapers.military_scraper import MilitaryScraper
from src.whatsapp.client import TelegramClient
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

SENT_CACHE_FILE = Path(__file__).parent.parent / 'data' / 'sent_cache.json'
SENT_CACHE_SIZE = 5  # number of recent URLs to remember per category


class AutoMonitor:
    """Main application class for AutoMonitor bot"""
    
    def __init__(self):
        self.settings = Settings()
        self.telegram_client = TelegramClient(self.settings)
        self.scrapers = self._initialize_scrapers()
        self.sent_urls: Dict[str, Deque[str]] = self._load_sent_cache()
        logger.info("AutoMonitor initialized successfully")

    def _load_sent_cache(self) -> Dict[str, Deque[str]]:
        """Load the persisted sent-URL cache from disk."""
        cache: Dict[str, Deque[str]] = {}
        try:
            if SENT_CACHE_FILE.exists():
                raw = json.loads(SENT_CACHE_FILE.read_text(encoding='utf-8'))
                for cat, urls in raw.items():
                    cache[cat] = deque(urls, maxlen=SENT_CACHE_SIZE)
                logger.info(f"Loaded sent cache ({sum(len(v) for v in cache.values())} entries)")
        except Exception as e:
            logger.warning(f"Could not load sent cache: {e}")
        return cache

    def _save_sent_cache(self) -> None:
        """Persist the current sent-URL cache to disk."""
        try:
            SENT_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
            data = {cat: list(urls) for cat, urls in self.sent_urls.items()}
            SENT_CACHE_FILE.write_text(json.dumps(data, indent=2), encoding='utf-8')
        except Exception as e:
            logger.warning(f"Could not save sent cache: {e}")
    
    def _initialize_scrapers(self) -> dict:
        """Initialize all enabled scrapers"""
        scrapers = {}
        
        if self.settings.ENABLE_TECH_NEWS:
            scrapers['tech'] = TechScraper()
            logger.info("Tech scraper enabled")
        
        if self.settings.ENABLE_SCIENCE_NEWS:
            scrapers['science'] = ScienceScraper()
            logger.info("Science scraper enabled")
        
        if self.settings.ENABLE_AI_NEWS:
            scrapers['ai'] = AIScraper()
            logger.info("AI scraper enabled")
        
        if self.settings.ENABLE_MILITARY_NEWS:
            scrapers['military'] = MilitaryScraper()
            logger.info("Military scraper enabled")
        
        return scrapers
    
    def run_scrapers(self):
        """Run all enabled scrapers and send updates via Telegram"""
        try:
            logger.info("Starting scraping cycle...")
            
            for category, scraper in self.scrapers.items():
                try:
                    logger.info(f"Scraping {category} news...")
                    articles = scraper.scrape()
                    
                    # Filter out recently-sent articles (last 5 per category)
                    category_name = scraper.category
                    recent = self.sent_urls.setdefault(
                        category_name, deque(maxlen=SENT_CACHE_SIZE)
                    )
                    new_articles = [
                        a for a in articles
                        if a.get('url') and a['url'] not in recent
                    ]

                    if new_articles:
                        self.telegram_client.send_news(category_name, new_articles)
                        for a in new_articles:
                            recent.append(a['url'])
                        self._save_sent_cache()
                        logger.info(f"Sent {len(new_articles)} new {category} articles via Telegram")
                    else:
                        logger.info(f"No new {category} articles to send (all match last {SENT_CACHE_SIZE} sent)")
                
                except Exception as e:
                    logger.error(f"Error scraping {category}: {str(e)}")
            
            logger.info("Scraping cycle completed")
        
        except Exception as e:
            logger.error(f"Unexpected error during scraping: {str(e)}")
    
    def schedule_jobs(self):
        """Schedule scraping jobs at regular intervals"""
        interval_seconds = self.settings.SCRAPE_INTERVAL
        interval_minutes = interval_seconds // 60
        
        schedule.every(interval_minutes).minutes.do(self.run_scrapers)
        logger.info(f"Scraping scheduled every {interval_minutes} minutes")
    
    def start(self):
        """Start the AutoMonitor bot"""
        try:
            logger.info("Starting AutoMonitor bot...")
            self.schedule_jobs()
            
            # Run immediately on startup
            self.run_scrapers()
            
            # Keep the scheduler running
            while True:
                schedule.run_pending()
                time.sleep(60)
        
        except KeyboardInterrupt:
            logger.info("AutoMonitor bot stopped by user")
        except Exception as e:
            logger.error(f"Critical error: {str(e)}")
            raise


def main():
    """Main entry point"""
    monitor = AutoMonitor()
    monitor.start()


if __name__ == "__main__":
    main()
