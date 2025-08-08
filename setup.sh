#!/bin/bash

echo "Setting up Pleione AI Assistant..."

# Check if Python 3.10+ is available
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python 3.10+ is required. Current version: $python_version"
    exit 1
fi

echo "✓ Python version check passed ($python_version)"

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Create necessary directories
echo "Creating project directories..."
mkdir -p backend/sandbox
mkdir -p backend/tests
mkdir -p logs

echo "✓ Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Start LM Studio and load a model on port 1234"
echo "2. Run './run.sh' to start the Pleione backend"
echo "3. Open http://localhost:8000/frontend/index.html in your browser"
echo ""
echo "Note: Make sure LM Studio is running before using the chat feature."
