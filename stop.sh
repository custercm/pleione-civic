#!/bin/bash

# Stop script to gracefully shutdown Pleione application

echo "🛑 Stopping Pleione..."

# Kill processes on port 8000 (where Pleione backend runs)
echo "Killing processes on port 8000..."
lsof -ti:8000 | xargs kill -TERM 2>/dev/null || true

# Kill any uvicorn processes specifically
echo "Stopping uvicorn processes..."
pkill -f "uvicorn.*backend.main" 2>/dev/null || true

# Kill any Python processes running our backend
echo "Stopping backend Python processes..."
pkill -f "python.*backend.main" 2>/dev/null || true

# Wait for graceful shutdown
sleep 2

# Force kill if still running
echo "Force killing any remaining processes on port 8000..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true

# Final check
if lsof -i:8000 > /dev/null 2>&1; then
    echo "⚠️  Warning: Some processes may still be running on port 8000"
    lsof -i:8000
else
    echo "✅ Pleione stopped successfully - port 8000 is free"
fi

echo "🏁 Stop complete"