# Deployment Guide

This guide covers deploying AutoMonitor to various free cloud platforms.

## Prerequisites

- GitHub account (for storing code)
- Telegram Bot Token (free from @BotFather)
- Git installed locally
- Code pushed to a GitHub repository

## ✅ COMPLETELY FREE DEPLOYMENT

All components are completely free:
- **Telegram API**: FREE (no per-message costs)
- **Cloud Hosting**: FREE (free tier)
- **Database**: FREE (free tier)
- **Total Cost**: **$0/month forever**

## Option 1: Deploy to Railway (Recommended)

Railway offers free tier with 500 hours/month.

### Steps

1. **Sign up at Railway.app**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create new project**
   - Click "Create New Project"
   - Select "Deploy from GitHub repo"
   - Select your AutoMonitor repository

3. **Configure environment variables**
   - Go to Project Settings
   - Add variables:
     - TELEGRAM_BOT_TOKEN
     - TELEGRAM_CHANNELS

4. **Deploy**
   - Railway automatically deploys on every push to main branch

## Option 2: Deploy to Render.com

Render offers free tier for Python apps.

### Steps

1. **Connect GitHub**
   - Go to [render.com](https://render.com)
   - Sign up and connect GitHub

2. **Create new service**
   - Select Python from templates
   - Connect your AutoMonitor repo

3. **Configure**
   - Add environment variables
   - Set start command: `python src/main.py`
   - Deploy

## Option 3: Deploy with Heroku

Heroku has paid tiers, but offers limited free tier.

### Alternative: Use Railway or Render instead (fully free)

## Option 4: Deploy with Docker

### Docker Setup

```bash
# Build image
docker build -t automonitor:latest .

# Run locally
docker run -d --env-file .env automonitor:latest

# Push to Docker Hub (optional)
docker tag automonitor:latest yourusername/automonitor:latest
docker push yourusername/automonitor:latest
```

## Option 5: Deploy to Replit

Replit offers free hosting with some limitations.

1. **Import from GitHub**
   - Go to [replit.com](https://replit.com)
   - Click "Import from GitHub"
   - Paste your AutoMonitor repo URL

2. **Configure**
   - Add secrets (environment variables)
   - Run: `pip install -r requirements.txt && python src/main.py`

## Setting Up Telegram Bot (Free)

1. **Create Bot**
   - Search for @BotFather in Telegram
   - Send `/newbot`
   - Follow prompts
   - Copy bot token

2. **Create Channels**
   - Create 4 channels: Tech, Science, AI, Military
   - Add your bot as admin
   - Get channel IDs from @userinfobot

3. **Get Credentials**
   - Bot Token: From @BotFather
   - Channel IDs: From @userinfobot (negative numbers)

4. **No cost ever!**
   - Telegram API is completely free
   - No per-message fees
   - Unlimited messaging

## Environment Variables for Deployment

```bash
TELEGRAM_BOT_TOKEN=your_token_from_botfather
TELEGRAM_CHANNELS=-1001234567890,-1009876543210,-1005555555555,-1008888888888
SCRAPE_INTERVAL=3600
ENABLE_TECH_NEWS=true
ENABLE_SCIENCE_NEWS=true
ENABLE_AI_NEWS=true
ENABLE_MILITARY_NEWS=true
LOG_LEVEL=INFO
ENVIRONMENT=production
DEBUG=false
```

## Monitoring and Logs

### Railway
- Real-time logs: Project > Deployments > View Log

### Render
- Logs: Service > Logs tab

### Docker
```bash
docker logs container_id
```

## Troubleshooting

### Bot not sending messages
1. Check Telegram bot token is correct
2. Verify channel IDs are correct (should be negative)
3. Check logs for errors
4. Ensure bot is admin in all channels

### Deployment fails
1. Check all environment variables are set
2. Verify requirements.txt has all dependencies
3. Check Python version compatibility (3.9+)
4. Review deployment logs

## Updating the Bot

```bash
# Make changes locally
git add .
git commit -m "Update bot"
git push origin main

# Cloud platform auto-deploys from main branch
# Or manually trigger deployment in platform console
```

## Cost Estimation

### AutoMonitor with Telegram
- **Railway**: FREE tier (500 hours/month = always on)
- **Telegram**: FREE API (unlimited messages)
- **Total**: **$0/month**

### Comparison with WhatsApp
- **WhatsApp + Twilio**: $5-10/month
- **Telegram**: $0/month
- **Monthly Savings**: $5-10 per month
- **Yearly Savings**: $60-120 per year

## Support

For deployment issues:
1. Check platform documentation
2. Review bot logs
3. Verify Telegram bot is working
4. Check network connectivity

---

**Note**: All components are free. No hidden costs or charges!

