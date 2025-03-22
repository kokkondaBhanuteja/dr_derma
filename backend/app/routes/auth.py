from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app.models.user import User
from app.services.auth_service import register_user, validate_login
from app.db.mysql import db

auth_bp = Blueprint('auth', __name__)

# Note: In __init__.py, these routes will be prefixed with /api/auth
# So the full routes will be /api/auth/register, /api/auth/login, etc.

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    print("🔍 Register route hit!")  # Debugging statement
    print("Received Data:", data)  # Logs received JSON data
    # Validate input data
    if not data or not data.get('email') or not data.get('password') or not data.get('username'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        # Register user
        user = register_user(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password')
        )
        
        # Generate access token
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'User registered successfully',
            'token': access_token,
            'user': user.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to register user'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Log in a user."""
    data = request.get_json()
    
    # Validate input data
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        # Validate login credentials
        user = validate_login(
            email=data.get('email'),
            password=data.get('password')
        )
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Update last login timestamp
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Generate access token
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'Login successful',
            'token': access_token,
            'user': user.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to log in'}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user."""
    try:
        # Get current user ID from token
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get user information'}), 500