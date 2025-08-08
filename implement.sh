#!/bin/bash

# Pleione Auto-Implementation Script (Git-based safety)
# This script automatically implements code that has passed tests

echo "🤖 Pleione Auto-Implementation (Git-based)"
echo "=========================================="

# Check if there are files in sandbox
SANDBOX_DIR="./backend/sandbox"
TEST_DIR="./backend/tests"

if [ ! -d "$SANDBOX_DIR" ] || [ -z "$(ls -A $SANDBOX_DIR 2>/dev/null)" ]; then
    echo "❌ No files found in sandbox directory"
    echo "   Generate some code first using the chat interface"
    exit 1
fi

echo "📁 Found files in sandbox:"
ls -la $SANDBOX_DIR

echo ""
echo "💾 Creating git backup first..."

# Ensure git repo exists and create backup
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "🔧 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit"
fi

# Create backup commit
git add .
if git commit -m "Backup before implementing sandbox code - $(date)"; then
    BACKUP_COMMIT=$(git rev-parse --short HEAD)
    echo "✅ Git backup created: $BACKUP_COMMIT"
    echo "   Rollback with: git reset --hard $BACKUP_COMMIT"
else
    echo "ℹ️ No changes to backup (already committed)"
fi

echo ""
echo "🧪 Running tests..."

# Run all tests in the test directory
if [ -d "$TEST_DIR" ] && [ -n "$(ls -A $TEST_DIR 2>/dev/null)" ]; then
    python3 -m pytest $TEST_DIR -v
    TEST_EXIT_CODE=$?
    
    if [ $TEST_EXIT_CODE -eq 0 ]; then
        echo "✅ All tests passed!"
        echo ""
        echo "🚀 Implementing code..."
        
        # Create generated directory if it doesn't exist
        mkdir -p ./backend/generated
        
        # Move all non-test files from sandbox to generated
        for file in $SANDBOX_DIR/*; do
            if [[ -f "$file" && ! "$(basename "$file")" =~ ^test_ ]]; then
                filename=$(basename "$file")
                cp "$file" "./backend/generated/$filename"
                echo "   ✅ Implemented: backend/generated/$filename"
            fi
        done
        
        echo ""
        echo "🎉 Implementation complete!"
        echo "   Generated code is now in: backend/generated/"
        echo "   Original files remain in sandbox for backup"
        echo ""
        echo "� Committing changes to git..."
        git add .
        git commit -m "Implemented tested code from sandbox - $(date)"
        NEW_COMMIT=$(git rev-parse --short HEAD)
        echo "✅ Changes committed: $NEW_COMMIT"
        echo ""
        echo "�📝 Next steps:"
        echo "   1. Review the implemented code in backend/generated/"
        echo "   2. Test the new functionality"
        echo "   3. Move files to their final locations if satisfied"
        echo "   4. Rollback with: git reset --hard $BACKUP_COMMIT (if needed)"
        
    else
        echo "❌ Tests failed! Implementation blocked for safety."
        echo "   Please review the test failures and fix the code."
        exit 1
    fi
else
    echo "⚠️  No tests found - implementing without testing (not recommended)"
    echo "   Continue anyway? (y/N)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "🚀 Implementing code without tests..."
        mkdir -p ./backend/generated
        for file in $SANDBOX_DIR/*; do
            if [[ -f "$file" ]]; then
                filename=$(basename "$file")
                cp "$file" "./backend/generated/$filename"
                echo "   ✅ Implemented: backend/generated/$filename"
            fi
        done
        echo "🎉 Implementation complete (without testing)!"
        echo ""
        echo "💾 Committing changes to git..."
        git add .
        git commit -m "Implemented code from sandbox (no tests) - $(date)"
        NEW_COMMIT=$(git rev-parse --short HEAD)
        echo "✅ Changes committed: $NEW_COMMIT"
        echo "   Rollback with: git reset --hard $BACKUP_COMMIT (if needed)"
    else
        echo "❌ Implementation cancelled"
        exit 1
    fi
fi
