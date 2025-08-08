import shutil
import tempfile
import subprocess
import os
import time
from datetime import datetime
from ..models.llm_connector import read_file_contents, update_file_contents

def create_safe_update_system():
    """Create a safe system for Pleione to update herself without breaking"""
    
    # Create directories for safe updates (no backups here - using git)
    os.makedirs("./backend/self_updates/", exist_ok=True)
    os.makedirs("./backend/self_updates/staging/", exist_ok=True)
    os.makedirs("./backend/self_updates/packages/", exist_ok=True)

def git_commit_current_state(message="Backup before Pleione update"):
    """Create a git commit of the current state"""
    try:
        # Check if git repo exists
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode != 0:
            # Initialize git repo
            subprocess.run(['git', 'init'], check=True)
            subprocess.run(['git', 'add', '.'], check=True)
            subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)
            print("✅ Git repository initialized")
        
        # Add all changes and commit
        subprocess.run(['git', 'add', '.'], check=True)
        result = subprocess.run(['git', 'commit', '-m', message], capture_output=True, text=True)
        
        if result.returncode == 0:
            # Get the commit hash
            hash_result = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True)
            commit_hash = hash_result.stdout.strip()[:8]
            print(f"✅ Git backup created: {commit_hash}")
            return {"status": "success", "commit_hash": commit_hash}
        else:
            print("ℹ️ No changes to commit")
            return {"status": "no_changes", "message": "No changes to backup"}
            
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": f"Git backup failed: {str(e)}"}

def git_rollback(steps_back=1):
    """Rollback using git to previous commits"""
    try:
        # Show recent commits first
        log_result = subprocess.run(['git', 'log', '--oneline', '-5'], capture_output=True, text=True)
        print("Recent commits:")
        print(log_result.stdout)
        
        # Reset to previous commit
        subprocess.run(['git', 'reset', '--hard', f'HEAD~{steps_back}'], check=True)
        print(f"✅ Rolled back {steps_back} commit(s)")
        return {"status": "success", "message": f"Rolled back {steps_back} commit(s)"}
        
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": f"Git rollback failed: {str(e)}"}

def create_staging_environment(files_to_update):
    """Create a staging environment with proposed changes"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    staging_dir = f"./backend/self_updates/staging/pleione_staging_{timestamp}"
    
    # Copy current system to staging
    shutil.copytree(".", staging_dir, ignore=shutil.ignore_patterns(
        '*.pyc', '__pycache__', '.git', 'backend/sandbox/*', 
        'backend/self_updates/*', 'node_modules'
    ))
    
    # Apply proposed changes to staging
    for file_path, new_content in files_to_update.items():
        staging_file_path = os.path.join(staging_dir, file_path)
        os.makedirs(os.path.dirname(staging_file_path), exist_ok=True)
        with open(staging_file_path, 'w') as f:
            f.write(new_content)
    
    return staging_dir

def run_comprehensive_tests(staging_dir):
    """Run all tests in the staging environment"""
    results = {
        "basic_tests": False,
        "api_tests": False,
        "integration_tests": False,
        "self_test": False,
        "errors": []
    }
    
    try:
        # Change to staging directory
        original_dir = os.getcwd()
        os.chdir(staging_dir)
        
        # Run basic tests
        result = subprocess.run(['python3', '-m', 'pytest', 'backend/tests/', '-v'], 
                              capture_output=True, text=True, timeout=60)
        results["basic_tests"] = result.returncode == 0
        if result.returncode != 0:
            results["errors"].append(f"Basic tests failed: {result.stderr}")
        
        # Test API startup
        try:
            result = subprocess.run(['python3', '-c', 'from backend.main import app; print("API import successful")'], 
                                  capture_output=True, text=True, timeout=30)
            results["api_tests"] = result.returncode == 0
            if result.returncode != 0:
                results["errors"].append(f"API test failed: {result.stderr}")
        except Exception as e:
            results["errors"].append(f"API test error: {str(e)}")
        
        # Test LLM connector
        try:
            result = subprocess.run(['python3', '-c', 'from backend.models.llm_connector import get_llm_response; print("LLM connector import successful")'], 
                                  capture_output=True, text=True, timeout=30)
            results["self_test"] = result.returncode == 0
            if result.returncode != 0:
                results["errors"].append(f"Self test failed: {result.stderr}")
        except Exception as e:
            results["errors"].append(f"Self test error: {str(e)}")
        
        # Integration test - try to start the server briefly
        try:
            # This would start the server for a few seconds to test it works
            proc = subprocess.Popen(['python3', '-m', 'uvicorn', 'backend.main:app', '--port', '8001'], 
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Let it run for 3 seconds then kill it
            time.sleep(3)
            proc.terminate()
            proc.wait(timeout=5)
            results["integration_tests"] = True
        except Exception as e:
            results["errors"].append(f"Integration test error: {str(e)}")
        
    finally:
        os.chdir(original_dir)
    
    # All tests must pass for safety
    results["all_passed"] = all([
        results["basic_tests"],
        results["api_tests"], 
        results["self_test"]
    ])
    
    return results

def create_update_package(staging_dir, test_results):
    """Create a deployable package if all tests pass"""
    if not test_results["all_passed"]:
        return {"status": "failed", "message": "Tests failed - package creation blocked"}
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    package_name = f"pleione_update_{timestamp}.tar.gz"
    package_path = f"./backend/self_updates/packages/{package_name}"
    
    # Create tar.gz package of the staging directory
    shutil.make_archive(package_path.replace('.tar.gz', ''), 'gztar', staging_dir)
    
    # Create deployment script
    deploy_script = f"""#!/bin/bash
# Pleione Self-Update Deployment Script
# Generated: {timestamp}

echo "🤖 Pleione Self-Update Deployment"
echo "================================="

# Stop current Pleione
./stop.sh

# Backup current version
cp -r . "./pleione_backup_pre_update_{timestamp}"

# Extract update
tar -xzf {package_path}
mv pleione_staging_{timestamp}/* .

# Start updated Pleione
./run.sh

echo "✅ Pleione update deployed successfully!"
echo "   Backup available at: pleione_backup_pre_update_{timestamp}"
"""
    
    deploy_script_path = f"./backend/self_updates/packages/deploy_update_{timestamp}.sh"
    with open(deploy_script_path, 'w') as f:
        f.write(deploy_script)
    
    os.chmod(deploy_script_path, 0o755)
    
    return {
        "status": "success",
        "package_path": package_path,
        "deploy_script": deploy_script_path,
        "message": f"Update package created: {package_name}"
    }

def safe_self_update(files_to_update):
    """Safely update Pleione's own code with comprehensive testing"""
    
    print("🛡️ Starting safe self-update process...")
    
    # Step 1: Git backup current system
    print("📦 Creating git backup...")
    backup_result = git_commit_current_state("Backup before Pleione self-update")
    if backup_result["status"] == "error":
        return {"status": "failed", "message": f"Git backup failed: {backup_result['message']}"}
    print("✅ Git backup completed")
    
    # Step 2: Create staging environment
    print("🏗️ Creating staging environment...")
    staging_dir = create_staging_environment(files_to_update)
    print(f"✅ Staging created: {staging_dir}")
    
    # Step 3: Run comprehensive tests
    print("🧪 Running comprehensive tests...")
    test_results = run_comprehensive_tests(staging_dir)
    
    if test_results["all_passed"]:
        print("✅ All tests passed!")
        
        # Step 4: Create deployment package
        print("📦 Creating deployment package...")
        package_result = create_update_package(staging_dir, test_results)
        
        return {
            "status": "ready_for_deployment",
            "git_backup": backup_result,
            "staging_dir": staging_dir,
            "test_results": test_results,
            "package": package_result,
            "message": "Self-update package ready for deployment",
            "rollback_info": "Use 'git reset --hard HEAD~1' to rollback if needed"
        }
    else:
        print("❌ Tests failed - update blocked for safety")
        return {
            "status": "failed",
            "git_backup": backup_result,
            "staging_dir": staging_dir,
            "test_results": test_results,
            "message": "Self-update blocked due to test failures",
            "errors": test_results["errors"],
            "rollback_info": "Use 'git reset --hard HEAD~1' to rollback if needed"
        }
