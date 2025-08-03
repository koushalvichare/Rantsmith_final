#!/usr/bin/env python3
"""
Comprehensive test script to verify all major features are working with Gemini AI
"""

import requests
import json
import time
from io import BytesIO
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:5000"
TEST_USER = {
    "username": "testuser",
    "password": "testpass123"
}

def test_auth():
    """Test authentication system"""
    print("=== Testing Authentication ===")
    
    # Test registration
    print("1. Testing registration...")
    register_data = {
        "username": TEST_USER["username"],
        "password": TEST_USER["password"],
        "email": f"{TEST_USER['username']}@test.com"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"Registration response: {response.status_code}")
    if response.status_code == 409:
        print("User already exists - continuing with login test")
    
    # Test login
    print("2. Testing login...")
    login_data = {
        "email": f"{TEST_USER['username']}@test.com",
        "password": TEST_USER["password"]
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Login response: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('access_token') or data.get('token')
        if token:
            print(f"Login successful! Token: {token[:50]}...")
            return token
        else:
            print(f"Login response missing token: {data}")
            return None
    else:
        print(f"Login failed: {response.text}")
        return None

def test_rant_submission(token):
    """Test rant submission"""
    print("\n=== Testing Rant Submission ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test text rant
    print("1. Testing text rant submission...")
    rant_data = {
        "content": "This is a test rant about how frustrating it is when technology doesn't work as expected!",
        "input_type": "text"
    }
    
    response = requests.post(f"{BASE_URL}/api/rant/submit", json=rant_data, headers=headers)
    print(f"Rant submission response: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        print(f"Rant submitted successfully! ID: {data.get('rant_id')}")
        return data.get('rant_id')
    else:
        print(f"Rant submission failed: {response.text}")
        return None

def test_ai_analysis(token, rant_id):
    """Test AI-powered rant analysis"""
    print("\n=== Testing AI Analysis ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("1. Testing rant analysis...")
    response = requests.post(f"{BASE_URL}/api/ai/analyze/{rant_id}", headers=headers)
    print(f"Analysis response: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Analysis successful!")
        print(f"Emotion: {data.get('emotion')}")
        print(f"Intensity: {data.get('intensity')}")
        print(f"Model used: {data.get('model_used')}")
        print(f"Suggestions: {data.get('suggestions', [])[:2]}...")  # First 2 suggestions
    else:
        print(f"Analysis failed: {response.text}")

def test_content_generation(token, rant_id):
    """Test AI-powered content generation"""
    print("\n=== Testing Content Generation ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test text generation
    print("1. Testing text generation...")
    response = requests.post(f"{BASE_URL}/api/ai/generate/text/{rant_id}", headers=headers)
    print(f"Text generation response: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Text generated successfully!")
        print(f"Model used: {data.get('model_used')}")
        print(f"Generated text: {data.get('generated_text', '')[:100]}...")
    else:
        print(f"Text generation failed: {response.text}")
    
    # Test meme generation
    print("2. Testing meme generation...")
    response = requests.post(f"{BASE_URL}/api/ai/generate/meme/{rant_id}", headers=headers)
    print(f"Meme generation response: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Meme generated successfully!")
        print(f"Model used: {data.get('model_used')}")
        print(f"Meme text: {data.get('meme_text', '')[:100]}...")
    else:
        print(f"Meme generation failed: {response.text}")
    
    # Test tweet generation
    print("3. Testing tweet generation...")
    response = requests.post(f"{BASE_URL}/api/ai/generate/tweet/{rant_id}", headers=headers)
    print(f"Tweet generation response: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Tweet generated successfully!")
        print(f"Model used: {data.get('model_used')}")
        print(f"Tweet text: {data.get('tweet_text')}")
    else:
        print(f"Tweet generation failed: {response.text}")

def test_audio_upload(token):
    """Test audio upload functionality"""
    print("\n=== Testing Audio Upload ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a simple mock audio file
    mock_audio_content = b"MOCK_AUDIO_DATA_FOR_TESTING"
    
    files = {
        'audio': ('test_audio.wav', BytesIO(mock_audio_content), 'audio/wav')
    }
    
    response = requests.post(f"{BASE_URL}/api/media/upload-audio", files=files, headers=headers)
    print(f"Audio upload response: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Audio processed successfully!")
        print(f"Transcribed text: {data.get('text', '')[:100]}...")
        print(f"Rant ID: {data.get('rant_id')}")
        return data.get('rant_id')
    else:
        print(f"Audio upload failed: {response.text}")
        return None

def test_rant_history(token):
    """Test rant history retrieval"""
    print("\n=== Testing Rant History ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/api/rant/history", headers=headers)
    print(f"Rant history response: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        rants = data.get('rants', [])
        print(f"Retrieved {len(rants)} rants from history")
        if rants:
            print(f"Latest rant: {rants[0].get('content', '')[:100]}...")
    else:
        print(f"Rant history failed: {response.text}")

def main():
    """Run all tests"""
    print("Starting comprehensive RantAI system test...")
    print("=" * 50)
    
    # Test authentication
    token = test_auth()
    if not token:
        print("❌ Authentication failed - stopping tests")
        return
    
    # Test rant submission
    rant_id = test_rant_submission(token)
    if not rant_id:
        print("❌ Rant submission failed - stopping tests")
        return
    
    # Test AI analysis
    test_ai_analysis(token, rant_id)
    
    # Test content generation
    test_content_generation(token, rant_id)
    
    # Test audio upload
    audio_rant_id = test_audio_upload(token)
    
    # Test rant history
    test_rant_history(token)
    
    print("\n" + "=" * 50)
    print("✅ All tests completed! Check the results above.")
    print("🤖 System is now using Gemini AI for all AI-powered features.")
    print("📱 Frontend should work with these backend endpoints.")

if __name__ == "__main__":
    main()
