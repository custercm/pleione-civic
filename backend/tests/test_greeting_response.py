# Filename: test_greeting_response.py

import unittest
from greeting_response import respond_to_greeting

class TestGreetingResponse(unittest.TestCase):
    
    def test_hello_greeting(self):
        """Test that 'hello' returns appropriate response"""
        result = respond_to_greeting("Hello")
        self.assertEqual(result, "Hello! I'm here to help you with your request.")
        
    def test_hi_greeting(self):
        """Test that 'hi' returns appropriate response"""
        result = respond_to_greeting("Hi")
        self.assertEqual(result, "Hello! I'm here to help you with your request.")
        
    def test_hey_greeting(self):
        """Test that 'hey' returns appropriate response"""
        result = respond_to_greeting("Hey")
        self.assertEqual(result, "Hello! I'm here to help you with your request.")
        
    def test_greetings_greeting(self):
        """Test that 'greetings' returns appropriate response"""
        result = respond_to_greeting("Greetings")
        self.assertEqual(result, "Hello! I'm here to help you with your request.")
        
    def test_mixed_case_greeting(self):
        """Test that mixed case greeting works"""
        result = respond_to_greeting("HELLO there!")
        self.assertEqual(result, "Hello! I'm here to help you with your request.")
        
    def test_whitespace_handling(self):
        """Test that whitespace is properly stripped"""
        result = respond_to_greeting("   Hello   ")
        self.assertEqual(result, "Hello! I'm here to help you with your request.")
        
    def test_non_greeting_message(self):
        """Test that non-greeting messages return appropriate response"""
        result = respond_to_greeting("How are you doing?")
        self.assertEqual(result, "I received your message, but it doesn't appear to be a greeting. How can I assist you?")
        
    def test_empty_string(self):
        """Test that empty string returns appropriate response"""
        result = respond_to_greeting("")
        self.assertEqual(result, "I received your message, but it doesn't appear to be a greeting. How can I assist you?")
        
    def test_type_error_handling(self):
        """Test that non-string input raises TypeError"""
        with self.assertRaises(TypeError):
            respond_to_greeting(123)
            
        with self.assertRaises(TypeError):
            respond_to_greeting(None)

if __name__ == "__main__":
    unittest.main()