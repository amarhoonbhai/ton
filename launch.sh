#!/bin/bash

# Activate virtual environment if needed
# source venv/bin/activate

echo "🚀 Starting FragmentGiftUpdate bot..."
nohup python3 bot_scheduler.py > bot_output.log 2>&1 &
echo "✅ Bot is running in the background. Logs: bot_output.log"