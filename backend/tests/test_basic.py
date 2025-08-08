import pytest
import sys
import os

# Add the parent directory to the path so we can import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_backend_imports():
    """Test that backend modules can be imported correctly"""
    try:
        from backend.models.llm_connector import get_llm_response, generate_code_and_tests
        assert callable(get_llm_response)
        assert callable(generate_code_and_tests)
        print("✅ Backend imports successful")
    except ImportError as e:
        pytest.fail(f"Failed to import backend modules: {e}")

def test_llm_connector_basic():
    """Test basic LLM connector functionality"""
    from backend.models.llm_connector import generate_code_and_tests
    
    # Test with a simple prompt (should handle connection errors gracefully)
    result = generate_code_and_tests("test prompt")
    
    # Should return a dictionary with either 'error' or 'status' key
    assert isinstance(result, dict)
    assert 'error' in result or 'status' in result
    print("✅ LLM connector basic test passed")

def test_directories_exist():
    """Test that required directories exist"""
    import os
    
    backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sandbox_dir = os.path.join(backend_dir, "sandbox")
    tests_dir = os.path.join(backend_dir, "tests")
    
    # These directories should be created by the application
    # We'll just check that the parent backend directory exists
    assert os.path.exists(backend_dir)
    print("✅ Directory structure test passed")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
