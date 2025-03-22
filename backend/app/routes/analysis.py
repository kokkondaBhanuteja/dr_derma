from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity,verify_jwt_in_request
import os
from werkzeug.utils import secure_filename
from datetime import datetime 
from flask_cors import cross_origin


from app.services.image_service import save_image, get_user_images, get_image_by_id, delete_image
from app.services.analysis_service import analyze_skin_image, get_analysis_by_image_id
from app.services.ai_service import generate_skincare_routine
from app.utils.validators import allowed_file
from app.db.mongodb import mongo


analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/analyze-skin', methods=['POST'])
@cross_origin()
def analyze_skin():
    try:
        # Validate JWT Token
        print("🔑 Checking JWT Token...")
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            print(f"✅ JWT Verified. User ID: {user_id}")
        except Exception as jwt_error:
            print(f"❌ JWT Error: {str(jwt_error)}")
            return jsonify({'error': f'Authentication error: {str(jwt_error)}'}), 401

        # Get and validate JSON data
        print("📦 Getting JSON data from request...")
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = ['skinType', 'concerns']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return jsonify({'error': f'Missing required field(s): {", ".join(missing_fields)}'}), 400

        # Ensure concerns is a list
        concerns = data.get('concerns', [])
        if isinstance(concerns, str):
            concerns = [concerns]
        elif not isinstance(concerns, list):
            return jsonify({'error': 'Concerns must be a list'}), 400

        # Process the data
        skin_data = {
            'skin_type': data.get('skinType', 'Unknown'),
            'concerns': ", ".join(concerns) if concerns else "None",
            'diet': data.get('diet', 'Unknown'),
            'hydration': data.get('hydration', 'Unknown'),
            'sleep': data.get('sleep', 'Unknown'),
            'lifestyle': data.get('lifestyle', 'Unknown')
        }

        print("🛠️ Processed Data for AI Model:", skin_data)

        # Generate skincare routine
        routine = generate_skincare_routine(
            skin_type=skin_data['skin_type'],
            concerns=skin_data['concerns']
        )

        analysis_result = {
            'skin_type': skin_data['skin_type'],
            'concerns': skin_data['concerns'],
            'recommendations': routine
        }

        try:
            mongo.db.analyses.insert_one({
                'user_id': user_id,
                'created_at': datetime.utcnow(),
                'analysis_result': analysis_result
            })
        except Exception as db_error:
            print(f"⚠️ Database warning: {str(db_error)}")

        return jsonify({
            'message': 'Skin analysis completed',
            'analysis': analysis_result
        }), 200

    except Exception as e:
        print(f"❌ Error processing request: {str(e)}")
        return jsonify({'error': f'Failed to analyze skin: {str(e)}'}), 500

    
@analysis_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_image():
    """Upload and analyze skin image."""
    try:
        # Check if image was uploaded
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Get current user ID from token
        user_id = get_jwt_identity()
        
        # Save image and get file ID
        filename = secure_filename(file.filename)
        file_id = save_image(user_id, file, filename)
        
        # Analyze image
        analysis_result = analyze_skin_image(file_id)
        
        return jsonify({
            'message': 'Image uploaded and analyzed successfully',
            'file_id': str(file_id),
            'analysis': analysis_result
        }), 201
    except Exception as e:
        return jsonify({'error': f'Failed to upload and analyze image: {str(e)}'}), 500


@analysis_bp.route('/images', methods=['GET'])
@jwt_required()
def get_images():
    """Get all user images."""
    try:
        user_id = get_jwt_identity()
        images = get_user_images(user_id)
        
        return jsonify({
            'images': images
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve images'}), 500

@analysis_bp.route('/images/<image_id>', methods=['GET'])
@jwt_required()
def get_image(image_id):
    """Get specific image by ID."""
    try:
        user_id = get_jwt_identity()
        image = get_image_by_id(image_id, user_id)
        
        if not image:
            return jsonify({'error': 'Image not found'}), 404
        
        return jsonify({
            'image': image
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve image'}), 500

@analysis_bp.route('/images/<image_id>', methods=['DELETE'])
@jwt_required()
def delete_image_endpoint(image_id):
    """Delete specific image by ID."""
    try:
        user_id = get_jwt_identity()
        success = delete_image(image_id, user_id)
        
        if not success:
            return jsonify({'error': 'Image not found or unauthorized'}), 404
        
        return jsonify({
            'message': 'Image deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to delete image'}), 500


@analysis_bp.route('/recommendations', methods=['GET'])
@jwt_required()
def get_recommendations():
    """Fetch personalized skincare recommendations."""
    try:
        user_id = get_jwt_identity()
        analysis_result = get_analysis_by_image_id(user_id)

        if not analysis_result:
            return jsonify({'error': 'No analysis found'}), 404

        # Use AI Service to generate a personalized routine
        skin_type = analysis_result.get("skin_type", "normal")
        concerns = analysis_result.get("concerns", [])
        allergies = analysis_result.get("allergies", "")

        routine = generate_skincare_routine(skin_type, concerns, allergies)

        return jsonify({
            'analysis': analysis_result,
            'routine': routine
        }), 200
    except Exception as e:
        return jsonify({'error': f'Failed to fetch recommendations: {str(e)}'}), 500