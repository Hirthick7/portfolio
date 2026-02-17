import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # MongoDB settings
    # For local MongoDB: 'mongodb://localhost:27017/'
    # For MongoDB Atlas: 'mongodb+srv://username:password@cluster.mongodb.net/'
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/'
    MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME') or 'portfolio_db'
    
    # Application settings
    DEBUG = os.environ.get('FLASK_DEBUG', 'True') == 'True'
    
    # Email settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or os.environ.get('MAIL_USERNAME')
    RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL') or 'mhirthick07@gmail.com'
