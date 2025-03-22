from app.models.user import User
from app.db.mysql import db
from app.utils.validators import validate_email, validate_password
import re

def register_user(username, email, password):
    """
    Register a new user.
    
    Args:
        username (str): User's username
        email (str): User's email
        password (str): User's password
        
    Returns:
        User: Newly created user object
        
    Raises:
        ValueError: If user with email or username already exists or invalid input
    """
    try:
        print('In the Service Method')
        # Validate email format
        if not validate_email(email):
            raise ValueError("Invalid email format")
        
        # Validate password strength
        if not validate_password(password):
            raise ValueError("Password must be at least 8 characters long and contain letters and numbers")
        
        # Validate username
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
            raise ValueError("Username must be 3-20 characters and contain only letters, numbers, and underscores")
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            raise ValueError("Email already registered")
        
        if User.query.filter_by(username=username).first():
            raise ValueError("Username already taken")
        
        # Create user
        user = User(
            username=username,
            email=email,
            password=password  # This will use the password.setter to hash the password
        )
        print('addint the User')
        db.session.add(user)
        print('Commiting')
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Error saving user:", str(e))
        raise ValueError("Failed to register user")
    return user


def validate_login(email, password):
    """
    Validate user login credentials.
    
    Args:
        email (str): User's email
        password (str): User's password
        
    Returns:
        User: User object if credentials are valid, None otherwise
    """
    user = User.query.filter_by(email=email).first()
    
    if user and user.verify_password(password):
        return user
    
    return None
