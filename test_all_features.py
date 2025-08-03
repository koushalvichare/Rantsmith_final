#!/usr/bin/env python3
"""
Comprehensive test script for RantAi - Tests all core features
"""

import requests
import json
import time
import os
from pathlib import Path

BASE_URL = "http://127.0.0.1:5000"
FRONTEND_URL = "http://localhost:3004"

def print_section(title):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")

def test_backend_health():
    """Test if backend is running and healthy"""
    print_section("Backend Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Backend is healthy")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        return False

def test_auth_endpoints():
    """Test authentication endpoints"""
    print_section("Authentication Tests")
    
    # Test registration
    try:
        register_data = {
            "username": "testuser123",
            "email": "test123@example.com",
            "password": "testpass123"
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code in [200, 201]:
            print("✅ Registration endpoint working")
        elif response.status_code == 409:
            print("⚠️  User already exists (expected)")
        else:
            print(f"❌ Registration failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Registration test failed: {e}")
    
    # Test login
    try:
        login_data = {
            "email": "test123@example.com",
            "password": "testpass123"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            print("✅ Login endpoint working")
            token = response.json().get('token')
            return token
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login test failed: {e}")
        return None

def test_rant_submission(token):
    """Test rant submission endpoint"""
    print_section("Rant Submission Tests")
    
    if not token:
        print("❌ No auth token available")
        return None
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Test text rant submission
    try:
        rant_data = {
            "content": "This is a test rant about how testing is so important but sometimes tedious!",
            "transformation_type": "poem",
            "tone": "neutral",
            "privacy": "private",
            "input_type": "text"
        }
        response = requests.post(f"{BASE_URL}/api/rant/submit", json=rant_data, headers=headers)
        if response.status_code in [200, 201]:
            print("✅ Rant submission working")
            rant_id = response.json().get('rant_id')
            print(f"Rant ID: {rant_id}")
            return rant_id
        else:
            print(f"❌ Rant submission failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Rant submission test failed: {e}")
        return None

def test_ai_processing(token, rant_id):
    """Test AI processing endpoints"""
    print_section("AI Processing Tests")
    
    if not token or not rant_id:
        print("❌ No auth token or rant ID available")
        return
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Test AI transformation
    try:
        transform_data = {
            "transformation_type": "poem",
            "output_format": "text"
        }
        response = requests.post(f"{BASE_URL}/api/media/transform-with-ai/{rant_id}", json=transform_data, headers=headers)
        if response.status_code == 200:
            print("✅ AI transformation working")
            result = response.json()
            print(f"Transformed text preview: {result.get('text', '')[:100]}...")
        else:
            print(f"❌ AI transformation failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ AI transformation test failed: {e}")

def test_media_endpoints(token):
    """Test media upload endpoints"""
    print_section("Media Upload Tests")
    
    if not token:
        print("❌ No auth token available")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test audio upload endpoint structure
    try:
        # Create a simple test audio file (empty for testing endpoint)
        test_audio_data = b"fake audio data for testing"
        files = {"audio": ("test.wav", test_audio_data, "audio/wav")}
        
        response = requests.post(f"{BASE_URL}/api/media/upload-audio", files=files, headers=headers)
        if response.status_code == 200:
            print("✅ Audio upload endpoint working")
        elif response.status_code == 400:
            print("⚠️  Audio upload endpoint exists but requires valid audio")
        else:
            print(f"❌ Audio upload failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Audio upload test failed: {e}")
    
    # Test image upload endpoint structure
    try:
        # Create a simple test image file (empty for testing endpoint)
        test_image_data = b"fake image data for testing"
        files = {"image": ("test.jpg", test_image_data, "image/jpeg")}
        
        response = requests.post(f"{BASE_URL}/api/media/upload-image", files=files, headers=headers)
        if response.status_code == 200:
            print("✅ Image upload endpoint working")
        elif response.status_code == 400:
            print("⚠️  Image upload endpoint exists but requires valid image")
        else:
            print(f"❌ Image upload failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Image upload test failed: {e}")

def test_frontend_connectivity():
    """Test frontend connectivity"""
    print_section("Frontend Connectivity Tests")
    
    try:
        response = requests.get(FRONTEND_URL)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend connection failed: {e}")

def test_cors_and_proxy():
    """Test CORS and proxy configuration"""
    print_section("CORS and Proxy Tests")
    
    try:
        # Test CORS preflight
        headers = {
            "Origin": FRONTEND_URL,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type,Authorization"
        }
        response = requests.options(f"{BASE_URL}/api/rant/submit", headers=headers)
        if response.status_code in [200, 204]:
            print("✅ CORS preflight working")
        else:
            print(f"⚠️  CORS preflight response: {response.status_code}")
    except Exception as e:
        print(f"❌ CORS test failed: {e}")

def check_environment_variables():
    """Check if required environment variables are set"""
    print_section("Environment Variables Check")
    
    # Check if .env file exists
    env_file = Path("c:/Users/ASUS/Desktop/projects/Python_Full_stack/RantAi/.env")
    if env_file.exists():
        print("✅ .env file exists")
        
        # Read and check key variables
        with open(env_file, 'r') as f:
            content = f.read()
            if "SECRET_KEY" in content:
                print("✅ SECRET_KEY found in .env")
            else:
                print("❌ SECRET_KEY missing from .env")
            
            if "GOOGLE_API_KEY" in content:
                print("✅ GOOGLE_API_KEY found in .env")
            else:
                print("❌ GOOGLE_API_KEY missing from .env")
    else:
        print("❌ .env file not found")

def main():
    """Run all tests"""
    print("🚀 Starting comprehensive RantAi feature tests...")
    
    # Check environment
    check_environment_variables()
    
    # Test backend health
    if not test_backend_health():
        print("\n❌ Backend is not healthy - stopping tests")
        return
    
    # Test frontend connectivity  
    test_frontend_connectivity()
    
    # Test CORS and proxy
    test_cors_and_proxy()
    
    # Test authentication
    token = test_auth_endpoints()
    
    # Test rant submission
    rant_id = test_rant_submission(token)
    
    # Test AI processing
    test_ai_processing(token, rant_id)
    
    # Test media endpoints
    test_media_endpoints(token)
    
    print_section("Test Summary")
    print("✅ = Working correctly")
    print("⚠️  = Partially working or expected behavior")
    print("❌ = Not working - needs investigation")
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    main()
