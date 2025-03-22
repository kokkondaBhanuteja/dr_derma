from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.user import User
from app.services.user_service import update_user_profile
from app.db.mysql import db

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile."""
    try:
        # Get current user ID from token
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'profile': user.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get profile information'}), 500

@profile_bp.route('/', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        # Get current user ID from token
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Update user profile
        updated_user = update_user_profile(user, data)
        
        return jsonify({
            'message': 'Profile updated successfully',
            'profile': updated_user.to_dict()
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to update profile'}), 500
