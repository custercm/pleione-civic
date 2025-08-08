# Filename: test_chat_clear_button.py

import tkinter as tk
from unittest.mock import patch, MagicMock
import sys
import os

# Add the current directory to path for importing chat_clear_button module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chat_clear_button import ChatInterface

def test_send_message():
    """Test sending a message"""
    root = tk.Tk()
    
    # Create instance of ChatInterface with mocked tkinter window
    app = ChatInterface(root)
    
    # Mock the entry field and text display to simulate user input
    with patch.object(app.message_entry, 'get', return_value='Hello world'):
        with patch.object(app.chat_display, 'config') as mock_config:
            with patch.object(app.chat_display, 'insert') as mock_insert:
                with patch.object(app.chat_display, 'see') as mock_see:
                    app.send_message()
                    
                    # Verify that text area was enabled and disabled
                    assert mock_config.call_count >= 2
                    assert mock_insert.called_once_with(tk.END, '[00:00:00] You: Hello world\n')
                    assert mock_see.called
                    
    root.destroy()

def test_clear_chat():
    """Test clearing chat messages"""
    root = tk.Tk()
    
    # Create instance of ChatInterface
    app = ChatInterface(root)
    
    with patch.object(app.chat_display, 'config') as mock_config:
        with patch.object(app.chat_display, 'delete') as mock_delete:
            app.clear_chat()
            
            # Verify that text area was enabled and disabled
            assert mock_config.call_count >= 2
            assert mock_delete.called_once_with(1.0, tk.END)
    
    root.destroy()

def test_clear_chat_empty():
    """Test clearing chat when it's already empty"""
    root = tk.Tk()
    
    # Create instance of ChatInterface with mocked tkinter window
    app = ChatInterface(root)
    
    # Mock the delete operation to simulate empty chat clearing
    with patch.object(app.chat_display, 'config') as mock_config:
        with patch.object(app.chat_display, 'delete') as mock_delete:
            app.clear_chat()
            
            assert mock_config.call_count >= 2
            assert mock_delete.called_once_with(1.0, tk.END)
    
    root.destroy()

def test_send_message_empty():
    """Test sending empty message"""
    root = tk.Tk()
    
    # Create instance of ChatInterface with mocked tkinter window
    app = ChatInterface(root)
    
    # Mock the entry field to simulate empty input
    with patch.object(app.message_entry, 'get', return_value=''):
        with patch.object(app.chat_display, 'config') as mock_config:
            app.send_message()
            
            # Verify that text area was never enabled for insert
            assert mock_config.call_count == 0
    
    root.destroy()

def test_send_message_with_special_characters():
    """Test sending message with special characters"""
    root = tk.Tk()
    
    app = ChatInterface(root)
    
    with patch.object(app.message_entry, 'get', return_value='Special chars: !@#$%^&*()'):
        with patch.object(app.chat_display, 'config') as mock_config:
            with patch.object(app.chat_display, 'insert') as mock_insert:
                app.send_message()
                
                assert mock_config.call_count >= 2
                assert mock_insert.called_once_with(tk.END, '[00:00:00] You: Special chars: !@#$%^&*()\n')
    
    root.destroy()

def run_tests():
    """Run all tests"""
    try:
        test_send_message()
        print("✓ send_message test passed")
        
        test_clear_chat()
        print("✓ clear_chat test passed")
        
        test_clear_chat_empty()
        print("✓ clear_chat empty test passed")
        
        test_send_message_empty()
        print("✓ send_message empty test passed")
        
        test_send_message_with_special_characters()
        print("✓ send_message with special chars test passed")
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    run_tests()