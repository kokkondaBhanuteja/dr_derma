from datetime import datetime
import bson.objectid as objectid

class Image:
    """Image model for MongoDB (not a SQLAlchemy model)."""
    
    @staticmethod
    def create_document(user_id, filename, analysis_result=None):
        """Create a new image document for MongoDB."""
        return {
            "user_id": user_id,
            "filename": filename,
            "upload_date": datetime.utcnow(),
            "analysis_result": analysis_result or {},
            "file_id": None  # Will be populated after GridFS storage
        }
    
    @staticmethod
    def from_mongo(mongo_doc):
        """Convert MongoDB document to dictionary."""
        if not mongo_doc:
            return None
            
        return {
            "id": str(mongo_doc.get("_id")),
            "user_id": mongo_doc.get("user_id"),
            "filename": mongo_doc.get("filename"),
            "upload_date": mongo_doc.get("upload_date").isoformat() if mongo_doc.get("upload_date") else None,
            "analysis_result": mongo_doc.get("analysis_result"),
            "file_id": str(mongo_doc.get("file_id")) if mongo_doc.get("file_id") else None
        }
