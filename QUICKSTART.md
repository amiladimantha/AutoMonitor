# Quick Start Guide

Get AutoMonitor running in 5 minutes!

## Local Setup

### 1. Prerequisites
- Python 3.9 or higher
- pip package manager
- Telegram account
- Git (optional)

### 2. Clone/Download Project
```bash
# If using git
git clone https://github.com/yourusername/AutoMonitor.git
cd AutoMonitor

# Or download ZIP and extract
```

### 3. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Telegram
```bash
# Get Telegram Bot Token
# 1. Open Telegram
# 2. Search for @BotFather
# 3. Send /newbot
# 4. Follow prompts to create bot
# 5. Copy the bot token

# Create Telegram Channels
# 1. Create channels for each category (Tech, Science, AI, Military)
# 2. Add your bot as admin
# 3. Get channel IDs (from @userinfobot in each channel)
```

### 6. Set up Environment Variables
```bash
# Copy template
cp .env.example .env

# Edit .env with your settings
# TELEGRAM_BOT_TOKEN=your_token_here
# TELEGRAM_CHANNELS=-1001234567890,-1009876543210
```

### 7. Run the Bot
```bash
python src/main.py
```

### 8. Monitor Logs
Logs appear in:
- Console (real-time)
- `logs/automonitor.log` (persistent)

## Getting Telegram Bot Token

### Step 1: Open Telegram
Download and install from [telegram.org](https://telegram.org) if not already installed.

### Step 2: Search for BotFather
In Telegram, search for **@BotFather** (official Telegram bot creator)

### Step 3: Create New Bot
- Send `/newbot` to @BotFather
- Choose a name for your bot (e.g., "AutoMonitor")
- Choose a username (must end with "bot", e.g., "AutoMonitor_bot")
- Copy the token you receive

### Step 4: Example Token
```
Your bot was created! Here is the token to access it:
1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefg
```

## Creating Telegram Channels

### Create Channels for Each Category
1. Open Telegram
2. Click "+" or menu → New Channel
3. Choose a name (e.g., "Tech News", "Science Updates")
4. Choose "Public" or "Private"
5. Add your bot as admin

### Get Channel IDs
```bash
# Method 1: Using @userinfobot
1. Go to your channel
2. Search for @userinfobot
3. Forward any message from your channel to it
4. It will show you the channel ID (e.g., -1001234567890)

# Method 2: Using web
1. Open https://www.t.me/your_channel_name
2. Check the URL for channel identifier
```

## Example Configuration

```bash
# .env file
TELEGRAM_BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefg
TELEGRAM_CHANNELS=-1001234567890,-1009876543210,-1005555555555,-1008888888888

# Tech: -1001234567890
# Science: -1009876543210  
# AI: -1005555555555
# Military: -1008888888888

ENABLE_TECH_NEWS=true
ENABLE_SCIENCE_NEWS=true
ENABLE_AI_NEWS=true
ENABLE_MILITARY_NEWS=true
SCRAPE_INTERVAL=3600
```

## First Run

1. Application starts
2. Creates logs directory
3. Runs scrapers immediately
4. Sends news articles to Telegram channels
5. Schedules next run based on SCRAPE_INTERVAL (default: 1 hour)
6. Continues running indefinitely

## Troubleshooting

### No messages being sent
- Check Telegram bot token in .env is correct
- Verify channel IDs are correct (must be negative numbers)
- Check logs: `tail logs/automonitor.log`
- Ensure bot is admin in all channels

### Bot token errors
- Verify token format: should be numbers:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefg
- Get new token from @BotFather if needed
- Don't share your token with anyone

### Channel ID issues
- Make sure channel IDs start with "-100"
- Get correct IDs from @userinfobot
- Private channels need negative IDs

### Import errors
- Ensure all requirements installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (needs 3.9+)

### Scraping errors
- Check internet connection
- Verify RSS feeds are accessible
- Some sites may require additional setup

## Next Steps

1. **Read full README**: See [README.md](README.md)
2. **Deploy to Cloud**: Follow [DEPLOYMENT.md](DEPLOYMENT.md)
3. **Customize**: Edit scrapers in `src/scrapers/`
4. **Contribute**: See [CONTRIBUTING.md](CONTRIBUTING.md)

## Commands Reference

```bash
# Run application
python src/main.py

# Run tests
python -m pytest tests/

# Check code style
pylint src/

# Package the project
python setup.py sdist

# With Docker
docker build -t automonitor .
docker run -d --env-file .env automonitor
```

## Support

- **Issues**: Create issue on GitHub
- **Questions**: Start a discussion
- **Bugs**: Report with full logs and error messages

## Resources

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/)
- [Schedule Library Docs](https://schedule.readthedocs.io/)
- [Python Documentation](https://docs.python.org/3/)

---

Happy scraping! 🤖📰
