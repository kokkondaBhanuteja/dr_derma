from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.routine import Routine
from app.db.mysql import db

routines_bp = Blueprint('routines', __name__)

@routines_bp.route('/', methods=['GET'])
@jwt_required()
def get_routines():
    """Get all user routines."""
    try:    
        user_id = get_jwt_identity()
        routines = Routine.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'routines': [routine.to_dict() for routine in routines]
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve routines'}), 500

@routines_bp.route('/<int:routine_id>', methods=['GET'])
@jwt_required()
def get_routine(routine_id):
    """Get specific routine by ID."""
    try:
        user_id = get_jwt_identity()
        routine = Routine.query.filter_by(id=routine_id, user_id=user_id).first()
        
        if not routine:
            return jsonify({'error': 'Routine not found'}), 404
        
        return jsonify({
            'routine': routine.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve routine'}), 500

@routines_bp.route('/', methods=['POST'])
@jwt_required()
def create_routine():
    """Create new skincare routine."""
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        user_id = get_jwt_identity()
        
        routine = Routine(
            user_id=user_id,
            name=data.get('name')
        )
        
        if data.get('morning_routine'):
            routine.morning_routine = data.get('morning_routine')
        
        if data.get('evening_routine'):
            routine.evening_routine = data.get('evening_routine')
        
        db.session.add(routine)
        db.session.commit()
        
        return jsonify({
            'message': 'Routine created successfully',
            'routine': routine.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create routine'}), 500

@routines_bp.route('/<int:routine_id>', methods=['PUT'])
@jwt_required()
def update_routine(routine_id):
    """Update existing skincare routine."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        user_id = get_jwt_identity()
        routine = Routine.query.filter_by(id=routine_id, user_id=user_id).first()
        
        if not routine:
            return jsonify({'error': 'Routine not found'}), 404
        
        if data.get('name'):
            routine.name = data.get('name')
        
        if 'morning_routine' in data:
            routine.morning_routine = data.get('morning_routine')
        
        if 'evening_routine' in data:
            routine.evening_routine = data.get('evening_routine')
        
        db.session.commit()
        
        return jsonify({
            'message': 'Routine updated successfully',
            'routine': routine.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update routine'}), 500

@routines_bp.route('/<int:routine_id>', methods=['DELETE'])
@jwt_required()
def delete_routine(routine_id):
    """Delete skincare routine."""
    try:
        user_id = get_jwt_identity()
        routine = Routine.query.filter_by(id=routine_id, user_id=user_id).first()
        
        if not routine:
            return jsonify({'error': 'Routine not found'}), 404
        
        db.session.delete(routine)
        db.session.commit()
        
        return jsonify({
            'message': 'Routine deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete routine'}), 500
