from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.db.mysql import db

class User(db.Model):
    """User model for storing user details."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    skin_type = db.Column(db.String(20))
    skin_concerns = db.Column(db.Text)
    allergies = db.Column(db.Text)
    
    # One-to-many relationship with routines
    routines = db.relationship('Routine', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def password(self):
        """Prevent password from being accessed."""
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """Set password to a hashed password."""
        self.password_hash = generate_password_hash(password,method='pbkdf2:sha256')

    def verify_password(self, password):
        """Check if password matches."""
        return check_password_hash(self.password_hash, password)

    def get_skin_concerns_list(self):
        """Convert string skin concerns to list."""
        if not self.skin_concerns:
            return []
        return [concern.strip() for concern in self.skin_concerns.split(',')]

    def set_skin_concerns_list(self, concerns_list):
        """Convert list of skin concerns to string."""
        if not concerns_list:
            self.skin_concerns = ''
        else:
            self.skin_concerns = ','.join(concerns_list)

    def to_dict(self):
        """Convert user model to dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'registered_on': self.registered_on.isoformat() if self.registered_on else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'skin_type': self.skin_type,
            'skin_concerns': self.get_skin_concerns_list(),
            'allergies': self.allergies
        }
