#!/bin/bash
# Start AutoMonitor bot in background using screen

SESSION_NAME="automonitor"

# Kill existing session if running
screen -X -S $SESSION_NAME quit 2>/dev/null

# Activate virtual environment
source venv/bin/activate

# Start bot in a detached screen session
screen -dmS $SESSION_NAME python run.py

echo "AutoMonitor bot started in background screen session: $SESSION_NAME"
echo ""
echo "Useful commands:"
echo "  View logs:     tail -f logs/automonitor.log"
echo "  Attach screen: screen -r $SESSION_NAME"
echo "  Detach screen: Ctrl+A then D"
echo "  Stop bot:      screen -X -S $SESSION_NAME quit"
