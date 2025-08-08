# Filename: test_hello.py

import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'sandbox'))
from hello import hello

class TestHello(unittest.TestCase):
    
    def test_hello_without_name(self):
        """Test hello function with no name parameter"""
        result = hello()
        self.assertEqual(result, "Hello World")
        
    def test_hello_with_name(self):
        """Test hello function with a name parameter"""
        result = hello("Alice")
        self.assertEqual(result, "Hello Alice")
        
    def test_hello_with_empty_string(self):
        """Test hello function with empty string"""
        result = hello("")
        self.assertEqual(result, "Hello ")
        
    def test_hello_with_none_value(self):
        """Test hello function with None value"""
        result = hello(None)
        self.assertEqual(result, "Hello World")
        
    def test_hello_with_invalid_type(self):
        """Test hello function with invalid type parameter"""
        with self.assertRaises(TypeError):
            hello(123)
            
        with self.assertRaises(TypeError):
            hello([])
            
        with self.assertRaises(TypeError):
            hello({"key": "value"})

if __name__ == "__main__":
    unittest.main()