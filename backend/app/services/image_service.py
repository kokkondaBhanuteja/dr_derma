import gridfs
from bson.objectid import ObjectId
from datetime import datetime
from flask import current_app

from app.db.mongodb import mongo
from app.models.image import Image

def save_image(user_id, file_obj, filename):
    """
    Save image to MongoDB GridFS.
    
    Args:
        user_id (int): User ID
        file_obj (FileStorage): File object from request
        filename (str): Filename to save
        
    Returns:
        str: ID of the saved image document
    """
    # Create image document
    image_doc = Image.create_document(user_id, filename)
    
    # Save file to GridFS
    fs = gridfs.GridFS(mongo.db)
    file_id = fs.put(file_obj, filename=filename)
    
    # Update image document with file ID
    image_doc["file_id"] = file_id
    
    # Save to MongoDB
    result = mongo.db.images.insert_one(image_doc)
    
    return result.inserted_id

def get_user_images(user_id):
    """
    Get all images for a user.
    
    Args:
        user_id (int): User ID
        
    Returns:
        list: List of image documents
    """
    images = list(mongo.db.images.find({"user_id": user_id}))
    return [Image.from_mongo(img) for img in images]

def get_image_by_id(image_id, user_id=None):
    """
    Get image by ID.
    
    Args:
        image_id (str): Image ID
        user_id (int, optional): User ID for verification
        
    Returns:
        dict: Image document or None if not found
    """
    try:
        query = {"_id": ObjectId(image_id)}
        if user_id is not None:
            query["user_id"] = user_id
            
        image = mongo.db.images.find_one(query)
        return Image.from_mongo(image)
    except:
        return None

def delete_image(image_id, user_id):
    """
    Delete image by ID.
    
    Args:
        image_id (str): Image ID
        user_id (int): User ID for verification
        
    Returns:
        bool: True if deleted, False otherwise
    """
    try:
        # Find image document
        image = mongo.db.images.find_one({
            "_id": ObjectId(image_id),
            "user_id": user_id
        })
        
        if not image:
            return False
        
        # Delete file from GridFS
        if image.get("file_id"):
            fs = gridfs.GridFS(mongo.db)
            fs.delete(image["file_id"])
        
        # Delete image document
        mongo.db.images.delete_one({"_id": ObjectId(image_id)})
        
        return True
    except:
        return False

def get_image_file(file_id):
    """
    Get image file from GridFS.
    
    Args:
        file_id (str): GridFS file ID
        
    Returns:
        tuple: (file_data, content_type) or None if not found
    """
    try:
        fs = gridfs.GridFS(mongo.db)
        file_obj = fs.get(ObjectId(file_id))
        return file_obj.read(), file_obj.content_type
    except:
        return None, None
