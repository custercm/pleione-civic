import requests
import json
import os
import re
import datetime
import subprocess

# Utility: List all files in the project
def list_project_files(root_dir=".", extensions=None):
    """Return a list of all files in the project, optionally filtered by extension(s)"""
    file_list = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if extensions:
                if any(filename.endswith(ext) for ext in extensions):
                    file_list.append(os.path.join(dirpath, filename))
            else:
                file_list.append(os.path.join(dirpath, filename))
    return file_list

# Utility: Read file contents
def read_file_contents(file_path, max_lines=200):
    """Read up to max_lines from a file and return as a string"""
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            return ''.join(lines[:max_lines])
    except Exception as e:
        return f"Error reading {file_path}: {str(e)}"

# Utility: Update file contents
def update_file_contents(file_path, new_content):
    """Overwrite file with new_content"""
    try:
        with open(file_path, 'w') as f:
            f.write(new_content)
        return True
    except Exception as e:
        return f"Error updating {file_path}: {str(e)}"

# LM Studio configuration
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
LM_STUDIO_MODEL = "local-model"  # This will use whatever model is loaded in LM Studio

# Timeout configurations (in seconds)
TIMEOUT_SIMPLE = 120      # 2 minutes for simple requests
TIMEOUT_COMPLEX = 600     # 10 minutes for complex code generation
TIMEOUT_MASSIVE = 900     # 15 minutes for large multi-file projects

def get_request_timeout(prompt, context_files=None):
    """Determine appropriate timeout based on request complexity"""
    # Count complexity factors
    complexity_score = 0
    
    # Length-based factors
    if len(prompt) > 1000:
        complexity_score += 2
    elif len(prompt) > 500:
        complexity_score += 1
    
    # Context files factor
    if context_files and len(context_files) > 3:
        complexity_score += 2
    elif context_files and len(context_files) > 1:
        complexity_score += 1
    
    # Keywords indicating complex operations
    complex_keywords = ['refactor', 'implement', 'create system', 'build application', 
                       'full project', 'multiple files', 'complex', 'advanced']
    if any(keyword in prompt.lower() for keyword in complex_keywords):
        complexity_score += 2
    
    # Return appropriate timeout
    if complexity_score >= 4:
        return TIMEOUT_MASSIVE
    elif complexity_score >= 2:
        return TIMEOUT_COMPLEX
    else:
        return TIMEOUT_SIMPLE

def get_llm_response(prompt, context_files=None):
    """Get response from LM Studio API with dynamic timeout based on complexity"""
    try:
        # Determine appropriate timeout
        timeout = get_request_timeout(prompt, context_files)
        print(f"🕐 Request complexity timeout: {timeout} seconds")
        
        messages = [
            {
                "role": "system",
                "content": "You are Pleione, a helpful AI assistant that generates safe, well-tested code. Always provide working code with proper error handling and include test cases."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        # If context files are provided, add them to the prompt
        if context_files:
            for file_path, file_content in context_files.items():
                messages.append({
                    "role": "user",
                    "content": f"Here is the current content of {file_path}:\n{file_content}"
                })
        payload = {
            "model": LM_STUDIO_MODEL,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Use dynamic timeout based on request complexity
        response = requests.post(LM_STUDIO_URL, json=payload, headers=headers, timeout=timeout)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"Error: LM Studio API returned status {response.status_code}"
    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to LM Studio. Please ensure LM Studio is running on port 1234."
    except requests.exceptions.Timeout:
        return "Error: Request to LM Studio timed out."
    except Exception as e:
        return f"Error connecting to LM Studio: {str(e)}"

def parse_and_save_code(llm_response, sandbox_dir, test_dir):
    """Parse LLM response and save code files to sandbox"""
    files_created = []
    
    # Enhanced prompt asks for specific format, so we parse it
    lines = llm_response.split('\n')
    current_section = None
    current_code = []
    current_filename = None
    
    for line in lines:
        # Look for code blocks
        if '```python' in line.lower():
            current_section = 'code'
            current_code = []
            continue
        elif '```' in line and current_section:
            # End of code block - save the file
            if current_code and current_filename:
                file_path = os.path.join(sandbox_dir if 'test_' not in current_filename else test_dir, current_filename)
                with open(file_path, 'w') as f:
                    f.write('\n'.join(current_code))
                files_created.append(file_path)
                print(f"✅ Created file: {file_path}")
            current_section = None
            current_code = []
            current_filename = None
            continue
        
        # Look for filename hints
        if current_section == 'code' and not current_filename:
            # Try to extract filename from comments
            if '# File:' in line or '# Filename:' in line:
                current_filename = line.split(':')[-1].strip()
            elif 'def ' in line and 'test_' in line:
                # This looks like a test function
                current_filename = f"test_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
            elif 'def ' in line or 'class ' in line:
                # This looks like main code
                current_filename = f"generated_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        
        if current_section == 'code':
            current_code.append(line)
    
    return files_created

def run_tests_and_validate(test_files):
    """Run tests and return results"""
    if not test_files:
        return {"status": "no_tests", "message": "No test files to run"}
    
    results = []
    all_passed = True
    
    for test_file in test_files:
        try:
            result = subprocess.run(
                ['python3', '-m', 'pytest', test_file, '-v'], 
                capture_output=True, 
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                results.append(f"✅ {test_file}: PASSED")
            else:
                results.append(f"❌ {test_file}: FAILED\n{result.stdout}\n{result.stderr}")
                all_passed = False
                
        except subprocess.TimeoutExpired:
            results.append(f"⏰ {test_file}: TIMEOUT")
            all_passed = False
        except Exception as e:
            results.append(f"💥 {test_file}: ERROR - {str(e)}")
            all_passed = False
    
    return {
        "status": "passed" if all_passed else "failed",
        "results": results,
        "all_passed": all_passed
    }

def auto_implement_code(sandbox_files, test_results):
    """Automatically implement code if tests pass"""
    if not test_results.get("all_passed", False):
        return {"status": "blocked", "message": "Tests failed - implementation blocked for safety"}
    
    implemented_files = []
    
    for file_path in sandbox_files:
        if 'test_' not in os.path.basename(file_path):
            # This is a main code file - move it to backend
            filename = os.path.basename(file_path)
            new_path = os.path.join("./backend/generated/", filename)
            
            # Create generated directory
            os.makedirs("./backend/generated/", exist_ok=True)
            
            # Copy file to generated directory
            with open(file_path, 'r') as src, open(new_path, 'w') as dst:
                dst.write(src.read())
            
            implemented_files.append(new_path)
            print(f"🚀 Implemented: {new_path}")
    
    return {
        "status": "implemented",
        "files": implemented_files,
        "message": f"Successfully implemented {len(implemented_files)} files"
    }
def generate_code_and_tests(prompt, files_to_include=None, max_retries=3):
    """Generate code and tests using LM Studio, iteratively fixing issues until tests pass"""
    # Create sandbox and tests directories if they don't exist
    sandbox_dir = "./backend/sandbox/"
    test_dir = "./backend/tests/"
    os.makedirs(sandbox_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)
    
    # Enhanced prompt for code generation
    enhanced_prompt = f"""
    Please help me with the following request: {prompt}
    
    Provide your response in the following format:
    1. A brief explanation of what you're creating
    2. The main code file content in ```python code blocks
    3. A corresponding test file content in ```python code blocks
    
    For each code block, include a comment like:
    # Filename: my_feature.py
    
    Make sure all code is production-ready with proper error handling.
    The test file should import from the correct relative path (../sandbox/filename).
    """
    
    # If files_to_include is provided, read their contents
    context_files = None
    if files_to_include:
        context_files = {}
        for file_path in files_to_include:
            context_files[file_path] = read_file_contents(file_path)
    
    for attempt in range(max_retries + 1):
        try:
            if attempt > 0:
                print(f"🔄 Attempt {attempt + 1}: Fixing issues...")
                
            llm_response = get_llm_response(enhanced_prompt, context_files=context_files)
            if llm_response.startswith("Error:"):
                return {"error": llm_response}
            
            # Parse and save code files automatically
            created_files = parse_and_save_code(llm_response, sandbox_dir, test_dir)
            
            # Separate test files from main files
            test_files = [f for f in created_files if 'test_' in os.path.basename(f)]
            code_files = [f for f in created_files if 'test_' not in os.path.basename(f)]
            
            # Run tests automatically
            test_results = run_tests_and_validate(test_files)
            
            # If tests pass, we're done!
            if test_results.get("all_passed", False) or test_results.get("status") == "no_tests":
                return {
                    "status": "generated", 
                    "response": llm_response + f"\n\n✅ Success after {attempt + 1} attempt(s)!",
                    "created_files": created_files,
                    "test_files": test_files,
                    "code_files": code_files,
                    "test_results": test_results,
                    "sandbox_dir": sandbox_dir,
                    "test_dir": test_dir,
                    "ready_for_implementation": True
                }
            
            # If tests failed and we have retries left, try to fix
            if attempt < max_retries:
                fix_prompt = f"""
                The previous code had test failures. Please fix the issues:
                
                Test Results:
                {chr(10).join(test_results.get('results', []))}
                
                Original Request: {prompt}
                
                Please provide corrected code that fixes these issues:
                1. Make sure imports work correctly (use sys.path.append for relative imports)
                2. Fix any syntax or logic errors
                3. Ensure tests can find and import the main code
                
                Provide the complete corrected files in the same format.
                """
                enhanced_prompt = fix_prompt
            
        except Exception as e:
            if attempt < max_retries:
                print(f"❌ Attempt {attempt + 1} failed: {e}, retrying...")
                continue
            else:
                return {"error": f"Code generation failed after {max_retries + 1} attempts: {str(e)}"}
    
    # If we get here, all retries failed
    return {
        "status": "generated", 
        "response": llm_response + f"\n\n⚠️ Generated code but tests still failing after {max_retries + 1} attempts. Manual review needed.",
        "created_files": created_files,
        "test_files": test_files,
        "code_files": code_files,
        "test_results": test_results,
        "sandbox_dir": sandbox_dir,
        "test_dir": test_dir,
        "ready_for_implementation": False
    }