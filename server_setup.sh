#!/bin/bash
# AutoMonitor Server Setup Script for Oracle Cloud Ubuntu

echo "=== AutoMonitor Server Setup ==="

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install -y python3 python3-pip python3-venv git screen

# Verify Python
python3 --version
pip3 --version

echo "=== System dependencies installed ==="

# Clone the repo (replace with your GitHub URL)
# git clone https://github.com/YOUR_USERNAME/AutoMonitor.git
# cd AutoMonitor

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

echo "=== Python dependencies installed ==="
echo ""
echo "Next steps:"
echo "1. Create your .env file: nano .env"
echo "2. Add your Telegram token and channel IDs"
echo "3. Run: chmod +x start.sh && ./start.sh"
