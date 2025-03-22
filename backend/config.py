import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-should-be-changed')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '844016a3b724c0d68dcc3df261abb8e7a32ff1c0a44a75ac042cdc76a07d2d34')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour

    MONGO_URI = os.getenv('MONGO_URI','mongodb://localhost:27017/dr_derma_db') 
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL','mysql+pymysql://root:Bhanu%402005@localhost:3306/dr_derma_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OpenAI API configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Make sure upload directory exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL')
    MONGODB_URI = os.getenv('MONGO_URI')

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
