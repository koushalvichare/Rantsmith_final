#!/usr/bin/env python3
"""Test script to debug authentication issues"""

import os
from dotenv import load_dotenv
from app import create_app, db
from app.models import User

def test_auth():
    """Test authentication functionality"""
    load_dotenv()
    
    app = create_app()
    with app.app_context():
        # Test user creation and password hashing
        test_user = User(
            username='authtest',
            email='authtest@example.com',
            display_name='Auth Test',
            bio='Test user for authentication',
            preferred_output_format='text',
            ai_personality='supportive'
        )
        test_user.set_password('testpass123')
        
        print("=== Authentication Test ===")
        print(f"Username: {test_user.username}")
        print(f"Email: {test_user.email}")
        print(f"Password hash: {test_user.password_hash}")
        print(f"Password check (correct): {test_user.check_password('testpass123')}")
        print(f"Password check (wrong): {test_user.check_password('wrongpass')}")
        
        # Check if user already exists
        existing_user = User.query.filter_by(email='authtest@example.com').first()
        if existing_user:
            print(f"User already exists: {existing_user.username}")
            print(f"Existing password check: {existing_user.check_password('testpass123')}")
        else:
            print("User does not exist, creating...")
            try:
                db.session.add(test_user)
                db.session.commit()
                print("User created successfully!")
            except Exception as e:
                print(f"Error creating user: {e}")
                db.session.rollback()

        # Test existing users
        print("\n=== Existing Users Test ===")
        existing_users = User.query.all()
        for user in existing_users[:3]:  # Test first 3 users
            print(f"Testing user: {user.username} ({user.email})")
            # Try common passwords
            for pwd in ['testpass123', '12345', 'password', 'test']:
                if user.check_password(pwd):
                    print(f"  ✓ Password '{pwd}' works for {user.username}")
                    break
            else:
                print(f"  ✗ No common password works for {user.username}")

if __name__ == '__main__':
    test_auth()
