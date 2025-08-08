#!/bin/bash

# Pleione Safe Self-Update Script (Git-based)
# This script allows Pleione to safely update herself using git for backups

echo "🛡️ Pleione Safe Self-Update System (Git-based)"
echo "=============================================="
echo ""

# Check if we're in the right directory
if [ ! -f "backend/main.py" ]; then
    echo "❌ Error: Please run this script from the Pleione root directory"
    exit 1
fi

# Check if git is available
if ! command -v git &> /dev/null; then
    echo "❌ Error: Git is required but not installed"
    exit 1
fi

echo "This script provides git-based safe update options:"
echo ""
echo "1. 📋 Show git status and recent commits"
echo "2. 💾 Create git backup (commit current state)"
echo "3. 🧪 Test an update package"
echo "4. 🚀 Deploy an update package"
echo "5. 🔄 Git rollback to previous version"
echo "6. 🧹 Clean up old staging files"
echo ""

read -p "Choose an option (1-6): " choice

case $choice in
    1)
        echo "📋 Git Status and Recent Commits:"
        echo "=================================="
        echo "Current status:"
        git status --short
        echo ""
        echo "Recent commits:"
        git log --oneline -10
        ;;
    
    2)
        echo "💾 Creating Git Backup"
        echo "======================"
        read -p "Enter commit message (or press Enter for default): " commit_msg
        
        if [ -z "$commit_msg" ]; then
            commit_msg="Manual backup before Pleione update - $(date)"
        fi
        
        git add .
        if git commit -m "$commit_msg"; then
            echo "✅ Git backup created successfully"
            git log --oneline -1
        else
            echo "ℹ️ No changes to commit"
        fi
        ;;
    
    3)
        echo "🧪 Testing Update Package"
        echo "========================="
        read -p "Enter package name (without path): " package_name
        
        if [ -f "backend/self_updates/packages/$package_name" ]; then
            echo "Testing package: $package_name"
            echo "✅ Package test completed (simulation)"
        else
            echo "❌ Package not found: $package_name"
        fi
        ;;
    
    4)
        echo "🚀 Deploying Update Package"
        echo "==========================="
        
        # First, ensure current state is committed
        if ! git diff-index --quiet HEAD --; then
            echo "⚠️  Uncommitted changes detected. Creating backup first..."
            git add .
            git commit -m "Auto-backup before deployment - $(date)"
        fi
        
        read -p "Enter package name to deploy: " package_name
        
        if [ -f "backend/self_updates/packages/deploy_$package_name" ]; then
            echo "⚠️  WARNING: This will update Pleione's code!"
            echo "   Current state is safely committed to git."
            echo "   You can rollback with: git reset --hard HEAD~1"
            read -p "Are you sure you want to proceed? (y/N): " confirm
            
            if [[ "$confirm" =~ ^[Yy]$ ]]; then
                # Execute the deployment script
                ./backend/self_updates/packages/deploy_$package_name
                
                # Commit the deployed changes
                git add .
                git commit -m "Deployed update package: $package_name"
                echo "✅ Update deployed and committed to git"
            else
                echo "❌ Deployment cancelled"
            fi
        else
            echo "❌ Deployment script not found: deploy_$package_name"
        fi
        ;;
    
    5)
        echo "🔄 Git Rollback to Previous Version"
        echo "==================================="
        echo "Recent commits:"
        git log --oneline -10
        echo ""
        read -p "How many commits back to rollback? (default: 1): " steps_back
        
        if [ -z "$steps_back" ]; then
            steps_back=1
        fi
        
        if ! [[ "$steps_back" =~ ^[0-9]+$ ]]; then
            echo "❌ Invalid number"
            exit 1
        fi
        
        echo "⚠️  WARNING: This will reset to $steps_back commit(s) ago!"
        echo "   All uncommitted changes will be lost."
        read -p "Are you sure? (y/N): " confirm
        
        if [[ "$confirm" =~ ^[Yy]$ ]]; then
            # Stop current instance
            ./stop.sh 2>/dev/null || true
            
            # Reset to previous commit
            git reset --hard HEAD~$steps_back
            
            # Start restored version
            ./run.sh &
            
            echo "✅ Rollback completed!"
            echo "   Restored to commit: $(git log --oneline -1)"
        else
            echo "❌ Rollback cancelled"
        fi
        ;;
    
    6)
        echo "🧹 Cleanup Old Staging Files"
        echo "============================"
        echo "This will remove old staging directories and packages"
        read -p "Proceed with cleanup? (y/N): " confirm
        
        if [[ "$confirm" =~ ^[Yy]$ ]]; then
            # Clean staging directories (keep last 3)
            if [ -d "backend/self_updates/staging" ]; then
                cd backend/self_updates/staging
                ls -t | tail -n +4 | xargs rm -rf 2>/dev/null || true
                cd ../../..
                echo "✅ Old staging directories cleaned"
            fi
            
            # Clean packages (keep last 5)
            if [ -d "backend/self_updates/packages" ]; then
                cd backend/self_updates/packages
                ls -t *.tar.gz 2>/dev/null | tail -n +6 | xargs rm -f 2>/dev/null || true
                ls -t deploy_*.sh 2>/dev/null | tail -n +6 | xargs rm -f 2>/dev/null || true
                cd ../../..
                echo "✅ Old packages cleaned"
            fi
            
            echo "✅ Cleanup completed!"
        else
            echo "❌ Cleanup cancelled"
        fi
        ;;
    
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "Git-based safe update process completed."
echo "💡 Tip: Use 'git log --oneline' to see all commits"
echo "💡 Tip: Use 'git reset --hard <commit-hash>' to go to any specific version"
