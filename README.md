# AutoMonitor - News Scraping Telegram Bot

An automated bot that scrapes web data related to technology, science, AI, and military updates, and sends categorized Telegram messages 24/7 on the cloud.

## Features

- **Multi-Category Web Scraping**: Scrapes tech updates, science breakthroughs, AI news, and military updates
- **Telegram Integration**: Sends categorized messages to Telegram channels (completely FREE)
- **Cloud-Ready**: Deployable on free cloud platforms (Railway, Render, Heroku, etc.)
- **24/7 Operation**: Runs continuously with scheduled scraping
- **Free and Open-Source**: Completely free to use and modify
- **Modular Architecture**: Easy to extend with new scrapers and features
- **Rich Formatting**: HTML formatted messages with clickable links

## Requirements

- Python 3.9+
- Telegram Bot Token (free from @BotFather)
- Cloud platform account (free tier)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AutoMonitor
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Telegram bot token and channel IDs
   ```

5. **Run the application**
   ```bash
   python src/main.py
   ```

## Configuration

Edit `.env` file with:
- Telegram bot token from @BotFather
- Telegram channel IDs (negative numbers like -1001234567890)
- Scraper settings
- Logging preferences

## Project Structure

```
AutoMonitor/
├── src/
│   ├── scrapers/          # Web scraping modules
│   ├── telegram/          # Telegram bot client
│   ├── config/            # Configuration files
│   ├── utils/             # Utility functions
│   └── main.py            # Main application entry point
├── tests/                 # Test files
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── Dockerfile             # Docker configuration
└── README.md              # This file
```

## Usage

### Running Locally

```bash
python src/main.py
```

### Running with Docker

```bash
docker build -t automonitor .
docker run -d --env-file .env automonitor
```

### Cloud Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed cloud deployment instructions.

## Getting Started with Telegram

1. **Create Telegram Account**: Download from [telegram.org](https://telegram.org)
2. **Create Bot**: Search for @BotFather in Telegram
3. **Get Token**: Send `/newbot` to BotFather, follow instructions
4. **Create Channels**: Create public or private channels for each news category
5. **Add Bot**: Add your bot as admin to your channels
6. **Get Channel IDs**: 
   - Send `/start` to @userinfobot in each channel
   - Copy the channel ID (negative number like -1001234567890)
7. **Configure .env**: Add your bot token and channel IDs

## Available News Categories

- **Tech Updates**: Latest technology news and gadgets
- **Science News**: Major scientific breakthroughs
- **AI Updates**: Artificial intelligence developments
- **Military News**: Global military and defense updates

## Cost

✅ **Completely FREE** - No charges ever!
- Telegram Bot API: FREE
- Cloud Hosting: FREE (free tier)
- Web Scraping: FREE
- **Total: $0/month**

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

This project is open-source and available under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue on the repository.

## Disclaimer

This bot is for informational purposes. Always verify information from official sources. Users are responsible for compliance with local laws and Telegram's terms of service.
