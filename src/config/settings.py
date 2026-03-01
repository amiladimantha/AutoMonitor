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
        # Primary recommended sources
        'https://feeds.arstechnica.com/arstechnica/index',       # Ars Technica - deep technical coverage
        'https://www.theverge.com/rss/index.xml',                # The Verge - fast consumer tech news
        'https://news.ycombinator.com/rss',                      # Hacker News - dev-curated top stories
        # Supplementary
        'https://feeds.feedburner.com/TechCrunch',
    ]
    
    SCIENCE_NEWS_SOURCES: list = [
        # Primary recommended sources
        'https://www.nature.com/nature.rss',                     # Nature - premier peer-reviewed journal
        'https://www.science.org/rss/news_current.xml',          # Science - top-tier research journal
        'https://www.technologyreview.com/feed/',                 # MIT Technology Review - science to commercialization
        'https://phys.org/rss-feed/',                            # Phys.org - physics, nano, space sciences
        # Supplementary
        'https://www.sciencedaily.com/rss/top/science.xml',
    ]
    
    AI_NEWS_SOURCES: list = [
        # Primary recommended sources
        'https://huggingface.co/blog/feed.xml',                  # Hugging Face Blog - open-source model releases
        'https://openai.com/blog/rss/',                          # OpenAI Blog - frontier model updates
        'https://www.anthropic.com/news/rss',                    # Anthropic News - safety & frontier research
        'https://deepmind.google/blog/rss.xml',                  # Google DeepMind Blog - research breakthroughs
        'https://www.deeplearning.ai/the-batch/feed/',           # The Batch (Andrew Ng) - curated AI trends
        'https://www.latent.space/feed',                         # Latent Space - AI engineering depth
        # Supplementary
        'https://venturebeat.com/category/ai/feed/',
    ]
    
    MILITARY_NEWS_SOURCES: list = [
        # Primary recommended sources
        'https://www.understandingwar.org/rss.xml',              # ISW - gold standard OSINT & operational analysis
        'https://acleddata.com/feed/',                           # ACLED - real-time conflict & protest data
        'https://www.cfr.org/rss/all-publications',             # CFR - strategic global conflict overview
        # Supplementary
        'https://www.militarytimes.com/arc/outboundfeeds/rss/?outputType=xml',
        'https://breakingdefense.com/feed/',
        'https://www.defensenews.com/arc/outboundfeeds/rss/?outputType=xml',
    ]
    
    # Request timeout (in seconds)
    REQUEST_TIMEOUT: int = 10
    
    # Maximum articles per category per cycle
    MAX_ARTICLES_PER_CATEGORY: int = 5

    # ----------------------------------------------------------------
    # LLM Deduplication
    # ----------------------------------------------------------------
    # Set OPENAI_API_KEY in your .env to enable LLM-powered grouping.
    # Without it the app falls back to fuzzy title similarity.
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')

    # Set to 'false' to disable dedup entirely
    ENABLE_LLM_DEDUP: bool = os.getenv('ENABLE_LLM_DEDUP', 'true').lower() == 'true'

    # OpenAI model used for grouping (gpt-4o-mini is fast and cheap)
    LLM_DEDUP_MODEL: str = os.getenv('LLM_DEDUP_MODEL', 'gpt-4o-mini')

    # Fuzzy fallback: titles with similarity >= this value are merged (0.0-1.0)
    DEDUP_SIMILARITY_THRESHOLD: float = float(os.getenv('DEDUP_SIMILARITY_THRESHOLD', '0.6'))
