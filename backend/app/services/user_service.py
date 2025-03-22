from app.models.user import User
from app.db.mysql import db
from app.utils.validators import validate_email

def update_user_profile(user, data):
    """
    Update user profile information.
    
    Args:
        user (User): User object to update
        data (dict): Dictionary containing profile data to update
        
    Returns:
        User: Updated user object
        
    Raises:
        ValueError: If email is invalid or already taken
    """
    # Update email if provided and different
    if 'email' in data and data['email'] != user.email:
        if not validate_email(data['email']):
            raise ValueError("Invalid email format")
            
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != user.id:
            raise ValueError("Email already registered")
            
        user.email = data['email']
    
    # Update skin type
    if 'skin_type' in data:
        user.skin_type = data['skin_type']
    
    # Update skin concerns
    if 'skin_concerns' in data:
        user.set_skin_concerns_list(data['skin_concerns'])
    
    # Update allergies
    if 'allergies' in data:
        user.allergies = data['allergies']
    
    db.session.commit()
    return user

def get_user_by_id(user_id):
    """
    Get user by ID.
    
    Args:
        user_id (int): User ID
        
    Returns:
        User: User object if found, None otherwise
    """
    return User.query.get(user_id)
