# Filename: test_chat_interface.py

import unittest
from tkinter import Tk
import chat_interface

class TestChatInterface(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.root = Tk()
        self.chat_app = chat_interface.ChatInterface(self.root)
    
    def tearDown(self):
        """Clean up after tests."""
        self.root.destroy()
    
    def test_clear_button_exists(self):
        """Test that clear button is created and exists in the interface."""
        # Check if clear button exists
        self.assertIsNotNone(self.chat_app.clear_button)
        self.assertEqual(self.chat_app.clear_button.cget("text"), "Clear")
    
    def test_send_message_functionality(self):
        """Test sending messages works properly."""
        # Test with a valid message
        original_count = len(self.chat_app.messages)
        
        # Set input text and send
        self.chat_app.text_entry.insert(0, "Hello World")
        self.chat_app.send_message()
        
        # Check that message was added to history
        self.assertEqual(len(self.chat_app.messages), original_count + 1)
        self.assertEqual(self.chat_app.messages[-1]["user"], "Hello World")
    
    def test_clear_chat_functionality(self):
        """Test clearing chat resets messages and display."""
        # Add some messages first
        self.chat_app.text_entry.insert(0, "Message 1")
        self.chat_app.send_message()
        
        self.chat_app.text_entry.insert(0, "Message 2")
        self.chat_app.send_message()
        
        # Verify messages exist before clearing
        self.assertEqual(len(self.chat_app.messages), 2)
        
        # Clear the chat
        self.chat_app.clear_chat()
        
        # Verify messages are cleared
        self.assertEqual(len(self.chat_app.messages), 0)
        
        # Verify display is cleared (should have no content)
        displayed_content = self.chat_app.chat_display.get(1.0, tk.END)
        self.assertEqual(displayed_content.strip(), "")
    
    def test_clear_chat_with_empty_input(self):
        """Test clearing chat when input field is empty."""
        # Clear chat without adding any messages
        self.chat_app.clear_chat()
        
        # Verify messages list is empty and display cleared
        self.assertEqual(len(self.chat_app.messages), 0)
        displayed_content = self.chat_app.chat_display.get(1.0, tk.END)
        self.assertEqual(displayed_content.strip(), "")
    
    def test_clear_button_command_error_handling(self):
        """Test that clear button command handles errors properly."""
        # This test ensures the method doesn't raise exceptions
        try:
            self.chat_app.clear_chat()
            self.assertTrue(True)  # If no exception, test passes
        except Exception as e:
            self.fail(f"Clear chat function raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()