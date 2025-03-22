import secrets
import string

def generate_random_string(length=32):
    """
    Generate a cryptographically secure random string.
    
    Args:
        length (int): Length of the string to generate
        
    Returns:
        str: Random string
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_api_key():
    """
    Generate an API key for external services.
    
    Returns:
        str: API key
    """
    return f"sk_{generate_random_string(32)}"

def sanitize_input(text):
    """
    Sanitize user input to prevent XSS and other attacks.
    
    Args:
        text (str): Input text
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    
    # Replace potentially dangerous characters
    replacements = {
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#x27;",
        "/": "&#x2F;",
        "\\": "&#x5C;"
    }
    
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    
    return text
