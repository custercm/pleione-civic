#!/bin/bash

echo "Starting Pleione backend on port 8000..."
echo "Make sure LM Studio is running on port 1234 before using the chat feature."

# Start the FastAPI backend
cd /Users/calebcuster/AI/pleione-civic
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

echo "Pleione backend started. Open http://localhost:8000/frontend/index.html to use the chat interface."