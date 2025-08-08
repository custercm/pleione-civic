import unittest
from chatbot import ChatBot

class TestChatBot(unittest.TestCase):
    """Test cases for the ChatBot class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.chatbot = ChatBot()
    
    def test_get_response_with_valid_message(self):
        """Test that get_response returns correct response for valid messages."""
        # Test case 1: Exact match
        result = self.chatbot.get_response("hello, test quick response")
        expected = "Hello! I'm responding quickly to your test message."
        self.assertEqual(result, expected)
        
        # Test case 2: Different casing
        result = self.chatbot.get_response("HELLO, TEST QUICK RESPONSE")
        expected = "Hello! I'm responding quickly to your test message."
        self.assertEqual(result, expected)
        
        # Test case 3: With whitespace
        result = self.chatbot.get_response("   hello, test quick response   ")
        expected = "Hello! I'm responding quickly to your test message."
        self.assertEqual(result, expected)
    
    def test_get_response_with_other_messages(self):
        """Test that get_response returns default response for other messages."""
        result = self.chatbot.get_response("hello")
        expected = "Hello there!"
        self.assertEqual(result, expected)
        
        result = self.chatbot.get_response("hi")
        expected = "Hi! How can I help you?"
        self.assertEqual(result, expected)
    
    def test_get_response_with_unknown_message(self):
        """Test that get_response returns default response for unknown messages."""
        result = self.chatbot.get_response("what is this?")
        expected = "I don't understand that message."
        self.assertEqual(result, expected)
    
    def test_get_response_with_invalid_input(self):
        """Test that get_response raises appropriate exceptions for invalid input."""
        # Test case 1: None input
        with self.assertRaises(ValueError):
            self.chatbot.get_response(None)
        
        # Test case 2: Empty string
        with self.assertRaises(ValueError):
            self.chatbot.get_response("")
        
        # Test case 3: Whitespace only
        with self.assertRaises(ValueError):
            self.chatbot.get_response("   ")
        
        # Test case 4: Non-string input
        with self.assertRaises(TypeError):
            self.chatbot.get_response(123)
    
    def test_is_valid_input(self):
        """Test that is_valid_input correctly identifies valid inputs."""
        # Valid inputs should return True
        self.assertTrue(self.chatbot.is_valid_input("hello, test quick response"))
        self.assertTrue(self.chatbot.is_valid_input("hello"))
        self.assertTrue(self.chatbot.is_valid_input("hi"))
        
        # Invalid inputs should return False
        self.assertFalse(self.chatbot.is_valid_input(None))
        self.assertFalse(self.chatbot.is_valid_input(""))
        self.assertFalse(self.chatbot.is_valid_input(123))

if __name__ == '__main__':
    unittest.main()