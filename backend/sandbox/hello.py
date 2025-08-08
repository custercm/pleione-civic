# Filename: hello.py

def hello(name=None):
    """
    Returns a greeting message.
    
    Args:
        name (str, optional): The name to greet. If None, returns "Hello World".
        
    Returns:
        str: A greeting message
        
    Raises:
        TypeError: If name is not a string or None
    """
    if name is not None and not isinstance(name, str):
        raise TypeError("name must be a string or None")
    
    if name is None:
        return "Hello World"
    else:
        return f"Hello {name}"

# Example usage
if __name__ == "__main__":
    print(hello())
    print(hello("Alice"))