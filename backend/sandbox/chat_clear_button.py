# Filename: chat_clear_button.py

import tkinter as tk
from tkinter import scrolledtext

class ChatInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Interface with Clear Button")
        self.root.geometry("500x400")
        
        # Create main frame
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create chat display area
        self.chat_display = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create input frame
        input_frame = tk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        # Create message entry field
        self.message_entry = tk.Entry(input_frame, width=50)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.message_entry.bind("<Return>", self.send_message)
        
        # Create send button
        self.send_button = tk.Button(input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=(0, 5))
        
        # Create clear button
        self.clear_button = tk.Button(input_frame, text="Clear", command=self.clear_chat)
        self.clear_button.pack(side=tk.RIGHT)
    
    def send_message(self, event=None):
        """Send message to chat display"""
        try:
            message = self.message_entry.get()
            if message.strip():
                # Enable the text area to insert new content
                self.chat_display.config(state=tk.NORMAL)
                
                # Insert the message with timestamp
                import datetime
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                self.chat_display.insert(tk.END, f"[{timestamp}] You: {message}\n")
                
                # Scroll to bottom
                self.chat_display.see(tk.END)
                
                # Disable the text area again
                self.chat_display.config(state=tk.DISABLED)
                
                # Clear the entry field
                self.message_entry.delete(0, tk.END)
        except Exception as e:
            print(f"Error sending message: {e}")
    
    def clear_chat(self):
        """Clear all chat messages"""
        try:
            # Enable text area to delete content
            self.chat_display.config(state=tk.NORMAL)
            
            # Delete all content
            self.chat_display.delete(1.0, tk.END)
            
            # Disable text area again
            self.chat_display.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Error clearing chat: {e}")

def main():
    root = tk.Tk()
    app = ChatInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()