import os
import io
import base64
from flask import current_app
import openai
from PIL import Image as PILImage

from app.services.image_service import get_image_file
from app.db.mongodb import mongo

def analyze_skin_image(file_id):
    """
    Analyze skin image using OpenAI's API.
    
    Args:
        file_id (str): GridFS file ID
        
    Returns:
        dict: Analysis results
    """
    # Get image file
    file_data, _ = get_image_file(file_id)
    if not file_data:
        raise ValueError("Image not found")
    
    # Load image and resize if needed
    image = PILImage.open(io.BytesIO(file_data))
    
    # Convert to base64 for OpenAI API
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    # Setup OpenAI API key
    openai.api_key = current_app.config["OPENAI_API_KEY"]
    
    # Send to OpenAI for analysis
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are a dermatologist assistant. Analyze the skin in the image and identify skin type, visible concerns, and possible conditions. Be factual and avoid dramatic language. Make clear these are observations only, not medical diagnosis."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this skin image and provide information about the skin type, visible concerns, and possible skincare recommendations"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_str}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        # Extract analysis result
        analysis_text = response.choices[0].message.content
        
        # Structure the result
        result = {
            "analysis": analysis_text,
            "recommendations": extract_recommendations(analysis_text)
        }
        
        # Update the image document with analysis results
        mongo.db.images.update_one(
            {"file_id": file_id},
            {"$set": {"analysis_result": result}}
        )
        
        return result
    except Exception as e:
        # Handle API errors
        return {
            "error": f"Analysis failed: {str(e)}",
            "recommendations": []
        }

def extract_recommendations(analysis_text):
    """
    Extract skincare recommendations from analysis text.
    
    Args:
        analysis_text (str): Analysis text from OpenAI
        
    Returns:
        list: List of recommendation strings
    """
    # This is a simple implementation - in production, you might want
    # to use a more sophisticated NLP approach or a secondary AI call
    recommendations = []
    
    # Look for recommendation sections
    lower_text = analysis_text.lower()
    
    if "recommend" in lower_text:
        # Split by sentences and look for recommendations
        sentences = analysis_text.split(".")
        for sentence in sentences:
            if "recommend" in sentence.lower():
                recommendations.append(sentence.strip() + ".")
    
    # If no explicit recommendations found, add a general note
    if not recommendations:
        recommendations.append("Please consult with a dermatologist for personalized recommendations.")
    
    return recommendations

def get_analysis_by_image_id(image_id, user_id):
    """
    Get analysis results for an image.
    
    Args:
        image_id (str): Image ID
        user_id (int): User ID for verification
        
    Returns:
        dict: Analysis results or None if not found
    """
    image = mongo.db.images.find_one(
        {"user_id": user_id, "analysis_result": {"$exists": True}},
        sort=[("_id", -1)]  # Get the latest image
    )

    if not image:
        return None

    return image.get("analysis_result")