
# Filename: chat_interface.py
import tkinter as tk
from tkinter import scrolledtext, messagebox
import json
import os

class ChatInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Interface")
        self.root.geometry("600x500")
        
        # Initialize chat history
        self.chat_history = []
        
        # Create main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create chat display area
        self.chat_display = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create input frame
        self.input_frame = tk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Create message entry field
        self.message_entry = tk.Entry(self.input_frame, width=50)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Create send button
        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=(0, 5))
        
        # Create clear button
        self.clear_button = tk.Button(self.input_frame, text="Clear", command=self.clear_chat)
        self.clear_button.pack(side=tk.RIGHT)
        
        # Bind Enter key to send message
        self.message_entry.bind('<Return>', lambda event: self.send_message())
    
    def add_to_chat_history(self, message, is_user=True):
        """Add a message to the chat history"""
        try:
            self.chat_history.append({
                'message': message,
                'is_user': is_user
            })
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add message: {str(e)}")
    
    def display_message(self, message, is_user=True):
        """Display a message in the chat window"""
        try:
            self.chat_display.config(state=tk.NORMAL)
            
            # Add styling for user vs bot messages
            if is_user:
                self.chat_display.insert(tk.END, f"You: {message}\n")
            else:
                self.chat_display.insert(tk.END, f"Bot: {message}\n")
                
            # Scroll to bottom
            self.chat_display.yview(tk.MOVETO, 1.0)
            
            # Disable text widget after adding message
            self.chat_display.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display message: {str(e)}")
    
    def send_message(self):
        """Handle sending a message"""
        try:
            message = self.message_entry.get().strip()
            
            if not message:
                messagebox.showwarning("Warning", "Please enter a message")
                return
            
            # Add user message to history
            self.add_to_chat_history(message, is_user=True)
            
            # Display user message
            self.display_message(message, is_user=True)
            
            # Simulate bot response (in real app this would be API call)
            bot_response = f"Received: {message}"
            self.add_to_chat_history(bot_response, is_user=False)
            self.display_message(bot_response, is_user=False)
            
            # Clear the entry field
            self.message_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {str(e)}")
    
    def clear_chat(self):
        """Clear all messages from chat history and display"""
        try:
            # Clear chat history
            self.chat_history.clear()
            
            # Clear the display area
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete(1.0, tk.END)
            self.chat_display.config(state=tk.DISABLED)
            
            messagebox.showinfo("Info", "Chat cleared successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear chat: {str(e)}")

def main():
    root = tk.Tk()
    app = ChatInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
