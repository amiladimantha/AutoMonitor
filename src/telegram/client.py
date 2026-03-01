"""Telegram bot client"""
from typing import List, Dict
import logging
import requests
from src.config.settings import Settings

logger = logging.getLogger(__name__)


class TelegramClient:
    """Client for sending messages via Telegram using HTTP API"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
        
        try:
            # Test the bot token
            response = requests.get(f"{self.api_url}/getMe", timeout=5)
            if response.status_code == 200:
                logger.info("Telegram bot initialized successfully")
            else:
                logger.error(f"Failed to connect to Telegram: {response.text}")
                self.bot_token = None
        except Exception as e:
            logger.error(f"Failed to initialize Telegram bot: {str(e)}")
            self.bot_token = None
    
    # Category emojis and labels
    CATEGORY_META = {
        'Technology':           {'emoji': '💻', 'label': 'Tech'},
        'Science':              {'emoji': '🔬', 'label': 'Science'},
        'AI & Machine Learning':{'emoji': '🧠', 'label': 'AI'},
        'Military & Defense':   {'emoji': '🪖', 'label': 'Military'},
    }

    def send_news(self, category: str, articles: List[Dict]):
        """Send news articles to the appropriate Telegram channel"""
        if not self.bot_token:
            logger.warning("Telegram bot not initialized. Skipping message send.")
            return
        
        if not articles:
            logger.info(f"No articles to send for category: {category}")
            return
        
        channel_id = self.settings.TELEGRAM_CHANNELS.get(category)
        if not channel_id:
            logger.warning(f"No channel configured for category: {category}")
            return
        
        # Send each article as its own rich message
        for article in articles[:5]:
            try:
                image_url = article.get('image')
                if image_url:
                    self._send_photo(channel_id, image_url, self._format_article(category, article))
                else:
                    self._send_message(channel_id, self._format_article(category, article))
            except Exception as e:
                # Fallback: send without image if photo fails
                try:
                    self._send_message(channel_id, self._format_article(category, article))
                except Exception as e2:
                    logger.error(f"Failed to send article to {category} channel: {str(e2)}")
        
        logger.info(f"Sent {len(articles)} articles to {category} channel ({channel_id})")
    
    def _format_article(self, category: str, article: Dict) -> str:
        """Format a single article (or merged digest) as a rich Telegram message."""
        meta = self.CATEGORY_META.get(category, {'emoji': '📰', 'label': category})
        emoji = meta['emoji']

        is_digest = article.get('source_count', 1) > 1
        merged_urls: list = article.get('merged_urls', [])

        title = self._safe_html(article.get('title', 'No title'))
        url = article.get('url', '')
        description = self._safe_html(article.get('description', ''))
        author = self._safe_html(article.get('author', ''))
        published = article.get('published', '')

        # Format published date (trim to just the date part)
        if published:
            published = published[:16].strip()  # e.g. "Sat, 28 Feb 2026"

        # Header — badge digest messages so readers know multiple sources agree
        if is_digest:
            source_count = article['source_count']
            msg = f"{emoji} <b>{title}</b>  <i>[{source_count} sources]</i>\n\n"
        else:
            msg = f"{emoji} <b>{title}</b>\n\n"

        if description:
            msg += f"{description}\n\n"

        # Metadata line
        meta_parts = []
        if author:
            meta_parts.append(f"✍️ {author}")
        if published:
            meta_parts.append(f"🕒 {published}")
        if meta_parts:
            msg += ' · '.join(meta_parts) + '\n\n'

        # Links — for digests show one labelled link per source
        if is_digest and len(merged_urls) > 1:
            msg += "🔗 <b>Sources:</b>\n"
            for src_url in merged_urls:
                host = src_url.split('/')[2].replace('www.', '') if '//' in src_url else src_url
                msg += f'  • <a href="{src_url}">{self._safe_html(host)}</a>\n'
        elif url:
            msg += f'🔗 <a href="{url}">Read Full Article</a>\n'

        msg += f'\n<i>🤖 AutoMonitor · #{meta["label"]}</i>'
        return msg
    
    def _safe_html(self, text: str) -> str:
        """Escape special HTML characters"""
        if not text:
            return ''
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    def _send_message(self, chat_id: int, text: str):
        """Send text message to Telegram channel via HTTP API"""
        url = f"{self.api_url}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    
    def _send_photo(self, chat_id: int, photo_url: str, caption: str):
        """Send a photo with caption to Telegram channel"""
        url = f"{self.api_url}/sendPhoto"
        # Telegram captions are limited to 1024 chars
        if len(caption) > 1024:
            caption = caption[:1020] + '...'
        data = {
            "chat_id": chat_id,
            "photo": photo_url,
            "caption": caption,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=data, timeout=15)
        response.raise_for_status()
        return response.json()
    
    def send_status(self, status: str):
        """Send status message to all channels"""
        if not self.bot_token:
            logger.warning("Telegram bot not initialized. Skipping status message.")
            return
        
        for category, channel_id in self.settings.TELEGRAM_CHANNELS.items():
            try:
                self._send_message(channel_id, status)
                logger.info(f"Status sent to {category} channel ({channel_id})")
            except Exception as e:
                logger.error(f"Failed to send status to {category} channel: {str(e)}")
