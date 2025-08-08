# Filename: greeting_response.py

def respond_to_greeting(message):
    """
    Responds to a greeting message with a friendly acknowledgment.
    
    Args:
        message (str): The input greeting message
        
    Returns:
        str: A response to the greeting
        
    Raises:
        TypeError: If message is not a string
    """
    if not isinstance(message, str):
        raise TypeError("Message must be a string")
    
    # Normalize the message by stripping whitespace and converting to lowercase
    normalized_message = message.strip().lower()
    
    # Check for common greeting patterns
    greetings = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']
    
    if any(greeting in normalized_message for greeting in greetings):
        return "Hello! I'm here to help you with your request."
    else:
        return "I received your message, but it doesn't appear to be a greeting. How can I assist you?"

# Example usage
if __name__ == "__main__":
    try:
        user_message = input("Enter your greeting: ")
        response = respond_to_greeting(user_message)
        print(response)
    except Exception as e:
        print(f"Error occurred: {e}")