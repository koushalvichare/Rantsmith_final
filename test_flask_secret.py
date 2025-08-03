#!/usr/bin/env python3
"""Test Flask app SECRET_KEY"""

import os
from dotenv import load_dotenv

def test_flask_secret():
    """Test Flask app SECRET_KEY"""
    # Clear any existing env var
    if 'SECRET_KEY' in os.environ:
        del os.environ['SECRET_KEY']
    
    # Load .env explicitly
    load_dotenv()
    
    env_secret = os.getenv('SECRET_KEY')
    print(f"Environment SECRET_KEY: {env_secret}")
    
    # Import after loading .env
    from app import create_app
    
    app = create_app()
    with app.app_context():
        flask_secret = app.config.get('SECRET_KEY')
        print(f"Flask app SECRET_KEY: {flask_secret}")
        print(f"Keys match: {env_secret == flask_secret}")

if __name__ == '__main__':
    test_flask_secret()
