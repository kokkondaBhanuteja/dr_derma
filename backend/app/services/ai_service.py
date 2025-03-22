import google.generativeai as genai
from flask import current_app
import json
import re
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def generate_skincare_routine(skin_type, concerns, location=None, allergies=None, diet_preferences=None):
    """
    Generate skincare routine and diet recommendations using Google's Gemini API.
    """
    api_key = os.getenv("GEMINI_API_KEY")  # Fetch from .env
    if not api_key:
        return {"error": "GEMINI_API_KEY is missing. Please check .env file."}
    
    genai.configure(api_key=api_key) 

    # Ensure concerns is a list before joining
    if not isinstance(concerns, list):
        concerns = [str(concerns)]  # Convert single value to list

    concerns_text = ", ".join(concerns) if concerns else "none"
    allergies_text = allergies if isinstance(allergies, str) else "none"
    location_text = location if isinstance(location, str) else "unknown"
    
    # Handle diet preferences
    if diet_preferences and isinstance(diet_preferences, list):
        diet_prefs_text = ", ".join(diet_preferences)
    elif diet_preferences and isinstance(diet_preferences, str):
        diet_prefs_text = diet_preferences
    else:
        diet_prefs_text = "no specific preferences"

    prompt = f"""
    Create a comprehensive skincare and diet plan for someone with {skin_type} skin.
    Their main skin concerns are: {concerns_text}.
    Their allergies are: {allergies_text}.
    They are located in: {location_text}.
    Their dietary preferences: {diet_prefs_text}.
    
    Please provide both morning and evening skincare routines, and diet recommendations considering their location and local food options.
    
    Return the response in the following JSON structure:
    {{
        "morning_routine": [
            {{"step": 1, "product_type": "Cleanser", "ingredients_to_look_for": ["ingredient1", "ingredient2"], "purpose": "Description"}}
        ],
        "evening_routine": [
            {{"step": 1, "product_type": "Cleanser", "ingredients_to_look_for": ["ingredient1", "ingredient2"], "purpose": "Description"}}
        ],
        "diet_recommendations": [
            {{
                "category": "Local Fruits and Vegetables",
                "description": "Focus on these nutrient-rich local options",
                "foods": [
                    {{"name": "Food name", "benefit": "How it helps skin"}}
                ]
            }}
        ]
    }}
    
    Include at least 5-7 steps in each skincare routine, and 3-5 diet recommendation categories with 3-4 specific foods in each.
    For the diet recommendations, focus on local foods available in their region that can help with their specific skin concerns.
    Only include the complete JSON in your response without any additional text or markdown formatting.
    """

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)

        # Extracting JSON response
        routine_text = response.text
        routine_text = re.sub(r'^```json\s*', '', routine_text)
        routine_text = re.sub(r'\s*```$', '', routine_text)
        print(routine_text)
        return json.loads(routine_text)

    except Exception as e:
        return {
            "error": f"Failed to generate routine: {str(e)}",
            "morning_routine": [],
            "evening_routine": [],
            "diet_recommendations": []
        }