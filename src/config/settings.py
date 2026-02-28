"""Configuration management for AutoMonitor"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings and configuration"""
    
    # Telegram Configuration - Channel mapping by category
    TELEGRAM_BOT_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHANNELS: dict = {
        'Technology': int(os.getenv('TELEGRAM_TECH_CHANNEL', 0)),
        'Science': int(os.getenv('TELEGRAM_SCIENCE_CHANNEL', 0)),
        'AI & Machine Learning': int(os.getenv('TELEGRAM_AI_CHANNEL', 0)),
        'Military & Defense': int(os.getenv('TELEGRAM_MILITARY_CHANNEL', 0)),
    }
    
    # Database Configuration
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///automonitor.db')
    
    # Scraper Configuration
    SCRAPE_INTERVAL: int = int(os.getenv('SCRAPE_INTERVAL', '3600'))  # 1 hour
    ENABLE_TECH_NEWS: bool = os.getenv('ENABLE_TECH_NEWS', 'true').lower() == 'true'
    ENABLE_SCIENCE_NEWS: bool = os.getenv('ENABLE_SCIENCE_NEWS', 'true').lower() == 'true'
    ENABLE_AI_NEWS: bool = os.getenv('ENABLE_AI_NEWS', 'true').lower() == 'true'
    ENABLE_MILITARY_NEWS: bool = os.getenv('ENABLE_MILITARY_NEWS', 'true').lower() == 'true'
    
    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = os.getenv('LOG_FILE', 'logs/automonitor.log')
    
    # Cloud Deployment
    ENVIRONMENT: str = os.getenv('ENVIRONMENT', 'development')
    DEBUG: bool = os.getenv('DEBUG', 'false').lower() == 'true'
    
    # Scraper URLs - Working RSS feeds for each category
    TECH_NEWS_SOURCES: list = [
        'https://feeds.arstechnica.com/arstechnica/index',
        'https://www.theverge.com/rss/index.xml',
        'https://feeds.feedburner.com/TechCrunch',
    ]
    
    SCIENCE_NEWS_SOURCES: list = [
        'https://www.sciencedaily.com/rss/top/science.xml',
        'https://rss.nytimes.com/services/xml/rss/nyt/Science.xml',
        'https://www.newscientist.com/feed/home/',
    ]
    
    AI_NEWS_SOURCES: list = [
        'https://venturebeat.com/category/ai/feed/',
        'https://www.artificialintelligence-news.com/feed/',
        'https://feeds.feedburner.com/aiweekly',
    ]
    
    MILITARY_NEWS_SOURCES: list = [
        'https://www.militarytimes.com/arc/outboundfeeds/rss/?outputType=xml',
        'https://breakingdefense.com/feed/',
        'https://www.defensenews.com/arc/outboundfeeds/rss/?outputType=xml',
    ]
    
    # Request timeout (in seconds)
    REQUEST_TIMEOUT: int = 10
    
    # Maximum articles per category per cycle
    MAX_ARTICLES_PER_CATEGORY: int = 5
