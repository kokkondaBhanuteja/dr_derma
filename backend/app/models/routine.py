from datetime import datetime
from app.db.mysql import db
import json

class Routine(db.Model):
    """Skincare routine model."""
    __tablename__ = 'routines'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Store routine data as JSON string
    morning_routine_json = db.Column(db.Text)
    evening_routine_json = db.Column(db.Text)
    
    @property
    def morning_routine(self):
        """Get morning routine as list of dictionaries."""
        if not self.morning_routine_json:
            return []
        return json.loads(self.morning_routine_json)
    
    @morning_routine.setter
    def morning_routine(self, routine_list):
        """Set morning routine from list of dictionaries."""
        if routine_list is None:
            self.morning_routine_json = None
        else:
            self.morning_routine_json = json.dumps(routine_list)
    
    @property
    def evening_routine(self):
        """Get evening routine as list of dictionaries."""
        if not self.evening_routine_json:
            return []
        return json.loads(self.evening_routine_json)
    
    @evening_routine.setter
    def evening_routine(self, routine_list):
        """Set evening routine from list of dictionaries."""
        if routine_list is None:
            self.evening_routine_json = None
        else:
            self.evening_routine_json = json.dumps(routine_list)
    
    def to_dict(self):
        """Convert routine model to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'morning_routine': self.morning_routine,
            'evening_routine': self.evening_routine
        }
