import subprocess
import os
import sys

def run_all_tests():
    """Run all tests in the tests directory"""
    test_dir = "./backend/tests/"
    
    # Create tests directory if it doesn't exist
    os.makedirs(test_dir, exist_ok=True)
    
    # Get all Python test files
    test_files = [f for f in os.listdir(test_dir) if f.endswith(".py") and f.startswith("test_")]
    
    if not test_files:
        print("📝 No test files found in ./backend/tests/")
        print("   Create test files starting with 'test_' to run automated tests.")
        return "No tests to run"
    
    print(f"Running {len(test_files)} test files...")
    results = []
    
    for file in test_files:
        test_path = os.path.join(test_dir, file)
        try:
            # Run pytest on the specific test file
            result = subprocess.run(
                [sys.executable, "-m", "pytest", test_path, "-v"], 
                capture_output=True, 
                text=True,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            
            if result.returncode == 0:
                success_msg = f"✅ Test {file} passed successfully"
                results.append(success_msg)
                print(success_msg)
            else:
                error_msg = f"❌ Test {file} failed:\n{result.stdout}\n{result.stderr}"
                results.append(error_msg)
                print(error_msg)
                
        except Exception as e:
            error_msg = f"💥 Error running test {file}: {str(e)}"
            results.append(error_msg)
            print(error_msg)
    
    return "\n".join(results)

if __name__ == "__main__":
    print("Pleione Test Runner")
    print("==================")
    result = run_all_tests()
    print("\nTest Summary:")
    print(result)