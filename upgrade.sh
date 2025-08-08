#!/bin/bash

echo "Pleione self-upgrade process starting..."

# Create sandbox and test directories if they don't exist
mkdir -p backend/sandbox 
mkdir -p backend/tests

echo "✓ Directories prepared"

# Run any pending tests to ensure current code is stable
echo "Running existing tests..."
python backend/test_runner.py

echo "✓ Tests completed"
echo ""
echo "Upgrade process completed."
echo "Generated code will be placed in backend/sandbox/ for manual review."
echo "Review and merge manually after testing."