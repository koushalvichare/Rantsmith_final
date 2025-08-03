#!/usr/bin/env python3
"""
Test script to verify frontend-backend integration
"""

import requests
import json
import time

# Test endpoints
BASE_URL = "http://localhost:5000"
FRONTEND_URL = "http://localhost:3002"

def test_backend_directly():
    """Test backend endpoints directly"""
    print("=== Testing Backend Directly ===")
    
    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
    
    # Test media test endpoint
    try:
        response = requests.get(f"{BASE_URL}/api/media/test")
        print(f"Media test: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Media test failed: {e}")
    
    print()

def test_frontend_proxy():
    """Test frontend proxy functionality"""
    print("=== Testing Frontend Proxy ===")
    
    # This would normally be done via browser, but we can test the proxy
    try:
        # Test if frontend is running
        response = requests.get(FRONTEND_URL)
        print(f"Frontend accessible: {response.status_code}")
    except Exception as e:
        print(f"Frontend not accessible: {e}")
    
    print()

def test_auth_flow():
    """Test the authentication flow"""
    print("=== Testing Authentication Flow ===")
    
    # Register a test user
    register_data = {
        "username": "testuser2",
        "email": "testuser2@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print(f"Registration: {response.status_code}")
        if response.status_code == 409:
            print("User already exists")
    except Exception as e:
        print(f"Registration failed: {e}")
    
    # Login
    login_data = {
        "email": "testuser2@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"Login: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token') or data.get('token')
            if token:
                print(f"Token received: {token[:50]}...")
                return token
            else:
                print(f"No token in response: {data}")
    except Exception as e:
        print(f"Login failed: {e}")
    
    return None

def test_rant_submission_with_token(token):
    """Test rant submission with authentication"""
    print("=== Testing Rant Submission ===")
    
    if not token:
        print("No token available, skipping rant submission test")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    rant_data = {
        "content": "This is a test rant from the integration test script!",
        "input_type": "text"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/rant/submit", json=rant_data, headers=headers)
        print(f"Rant submission: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            rant_id = data.get('rant_id')
            print(f"Rant ID: {rant_id}")
            return rant_id
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Rant submission failed: {e}")
    
    return None

def test_ai_features_with_token(token, rant_id):
    """Test AI features with authentication"""
    print("=== Testing AI Features ===")
    
    if not token or not rant_id:
        print("No token or rant_id available, skipping AI tests")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test analysis
    try:
        response = requests.post(f"{BASE_URL}/api/ai/analyze/{rant_id}", headers=headers)
        print(f"AI Analysis: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Analysis result: {data}")
    except Exception as e:
        print(f"AI Analysis failed: {e}")
    
    # Test text generation
    try:
        response = requests.post(f"{BASE_URL}/api/ai/generate/text/{rant_id}", headers=headers)
        print(f"Text Generation: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Generated text: {data.get('generated_text', '')[:100]}...")
    except Exception as e:
        print(f"Text generation failed: {e}")

def main():
    """Run all tests"""
    print("🚀 Starting Frontend-Backend Integration Tests")
    print("=" * 60)
    
    # Test backend directly
    test_backend_directly()
    
    # Test frontend accessibility
    test_frontend_proxy()
    
    # Test authentication flow
    token = test_auth_flow()
    
    # Test rant submission
    rant_id = test_rant_submission_with_token(token)
    
    # Test AI features
    test_ai_features_with_token(token, rant_id)
    
    print("=" * 60)
    print("✅ Integration tests completed!")
    print("\n📋 Manual Testing Steps:")
    print("1. Open browser to http://localhost:3002")
    print("2. Register/Login with a test account")
    print("3. Try submitting a rant")
    print("4. Try uploading audio/image")
    print("5. Check if AI features work")
    print("6. Test the debug buttons in MediaUpload component")

if __name__ == "__main__":
    main()
