import os
import uuid
from flask import current_app
from werkzeug.utils import secure_filename

def generate_unique_filename(filename):
    """
    Generate a unique filename to prevent collisions.
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Unique filename
    """
    # Get extension
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    # Generate unique name
    unique_name = f"{uuid.uuid4().hex}"
    
    # Return with extension if available
    if ext:
        return f"{unique_name}.{ext}"
    return unique_name

def get_file_path(filename):
    """
    Get full path for a file in the upload directory.
    
    Args:
        filename (str): Filename
        
    Returns:
        str: Full file path
    """
    return os.path.join(current_app.config["UPLOAD_FOLDER"], filename)

def format_routine_step(step_data):
    """
    Format a routine step for display.
    
    Args:
        step_data (dict): Step data
        
    Returns:
        dict: Formatted step data
    """
    return {
        "step": step_data.get("step", 0),
        "product_type": step_data.get("product_type", ""),
        "ingredients": step_data.get("ingredients_to_look_for", []),
        "purpose": step_data.get("purpose", "")
    }
