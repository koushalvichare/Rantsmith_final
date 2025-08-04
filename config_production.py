"""
Production configuration for Render deployment
"""
import os
from datetime import timedelta

class ProductionConfig:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-secret-key-change-me'
    DEBUG = False
    TESTING = False
    
    # Database
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///rantsmith.db'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AI Service API Keys
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY') or os.environ.get('GEMINI_API_KEY')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')
    RUNWAYML_API_KEY = os.environ.get('RUNWAYML_API_KEY')
    
    # File uploads
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', '16777216'))  # 16MB
    
    # Server settings
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT', 5000))
    
    # CORS settings for production
    CORS_ORIGINS = [
        "https://your-frontend-domain.vercel.app",  # Replace with your actual Vercel domain
        "http://localhost:3000",  # For development
        "http://localhost:3001"   # For development
    ]
    
    # Security headers
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(hours=1)
    
    # JWT settings
    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
