#!/bin/bash

echo "🚀 Starting Pleione..."

# First, stop any existing instances
echo "Stopping any existing Pleione instances..."
./stop.sh

# Wait a moment for cleanup
sleep 1

# Check if port 8000 is free
if lsof -i:8000 > /dev/null 2>&1; then
    echo "❌ Port 8000 is still in use. Force clearing..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    sleep 1
fi

# Verify LM Studio connection (optional check)
echo "🔍 Checking LM Studio on port 1234..."
if curl -s http://localhost:1234/v1/models > /dev/null 2>&1; then
    echo "✅ LM Studio is running on port 1234"
else
    echo "⚠️  Warning: LM Studio may not be running on port 1234"
    echo "   Make sure LM Studio is started and serving a model before using chat features"
fi

echo "🏃 Starting Pleione backend on port 8000..."

# Start the FastAPI backend
cd /Users/calebcuster/AI/pleione-civic
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

echo "✅ Pleione backend started. Open http://localhost:8000 to use the interface."