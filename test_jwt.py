#!/usr/bin/env python3
"""Test JWT token functionality"""

import os
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

def test_jwt():
    """Test JWT token generation and verification"""
    load_dotenv()
    
    secret_key = os.getenv('SECRET_KEY', 'fallback-secret')
    print(f"SECRET_KEY: {secret_key}")
    
    # Generate token
    payload = {
        'user_id': 9,
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    print(f"Generated token: {token}")
    
    # Verify token
    try:
        decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
        print(f"Decoded payload: {decoded}")
        print("JWT verification successful!")
    except jwt.ExpiredSignatureError:
        print("Token has expired")
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {e}")
    
    # Test with the actual token from login
    test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo5LCJleHAiOjE3NTI0OTU3OTV9.BVZUzUUr_vKsuy-gL9mqSdQEz7c993aWpIa1Ul1E1mPs"
    print(f"\nTesting login token: {test_token}")
    
    try:
        decoded = jwt.decode(test_token, secret_key, algorithms=['HS256'])
        print(f"Login token decoded: {decoded}")
        print("Login token verification successful!")
    except jwt.ExpiredSignatureError:
        print("Login token has expired")
    except jwt.InvalidTokenError as e:
        print(f"Login token invalid: {e}")

if __name__ == '__main__':
    test_jwt()
