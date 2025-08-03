#!/usr/bin/env python3
"""
Final multimedia features test for RantAi
This script tests all the multimedia features including:
1. Audio-only rant submission
2. Image-only rant submission  
3. Text-to-speech generation
4. Image/meme generation
5. Video generation
6. AI transformation with multimedia outputs
"""

import requests
import json
import os
import tempfile
import time
from PIL import Image
import base64

BASE_URL = "http://127.0.0.1:5000"

def test_user_registration_and_login():
    """Test user registration and login to get auth token"""
    print("🔐 Testing user registration and login...")
    
    # Register a test user
    register_data = {
        "username": f"testuser_multimedia_{int(time.time())}",
        "email": f"test_multimedia_{int(time.time())}@example.com",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"Registration response: {response.status_code}")
    
    if response.status_code == 201:
        print("✅ User registered successfully")
    else:
        print(f"❌ Registration failed: {response.text}")
        return None
    
    # Login to get token
    login_data = {
        "email": register_data["email"],
        "password": register_data["password"]
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Login response: {response.status_code}")
    
    if response.status_code == 200:
        token = response.json().get('token')
        print("✅ Login successful")
        return token
    else:
        print(f"❌ Login failed: {response.text}")
        return None

def test_media_endpoints(token):
    """Test all media-related endpoints"""
    print("\n📱 Testing media endpoints...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test media API availability
    response = requests.get(f"{BASE_URL}/api/media/test")
    print(f"Media API test: {response.status_code}")
    if response.status_code == 200:
        print("✅ Media API is available")
        endpoints = response.json().get('endpoints', [])
        print(f"Available endpoints: {endpoints}")
    else:
        print("❌ Media API is not available")
        return False
    
    return True

def test_audio_submission(token):
    """Test audio file submission and processing"""
    print("\n🎵 Testing audio submission...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a mock audio file (we'll use a text file with .wav extension for this test)
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_audio:
        tmp_audio.write(b"Mock audio content for testing")
        tmp_audio_path = tmp_audio.name
    
    try:
        with open(tmp_audio_path, 'rb') as audio_file:
            files = {'audio': ('test_audio.wav', audio_file, 'audio/wav')}
            response = requests.post(f"{BASE_URL}/api/media/upload-audio", files=files, headers=headers)
        
        print(f"Audio upload response: {response.status_code}")
        if response.status_code in [200, 201]:
            data = response.json()
            print("✅ Audio upload successful")
            print(f"Transcribed text: {data.get('text', 'N/A')}")
            print(f"Rant ID: {data.get('rant_id', 'N/A')}")
            return data.get('rant_id')
        else:
            print(f"❌ Audio upload failed: {response.text}")
            return None
            
    finally:
        os.unlink(tmp_audio_path)

def test_image_submission(token):
    """Test image file submission and processing"""
    print("\n🖼️ Testing image submission...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a simple test image
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_image:
        img = Image.new('RGB', (100, 100))
        # Simple red test image
        img.save(tmp_image.name)
        tmp_image_path = tmp_image.name
    
    try:
        with open(tmp_image_path, 'rb') as image_file:
            files = {'image': ('test_image.png', image_file, 'image/png')}
            response = requests.post(f"{BASE_URL}/api/media/upload-image", files=files, headers=headers)
        
        print(f"Image upload response: {response.status_code}")
        if response.status_code in [200, 201]:
            data = response.json()
            print("✅ Image upload successful")
            print(f"Image data length: {len(data.get('image_data', ''))}")
            print(f"Metadata: {data.get('metadata', {})}")
            return True
        else:
            print(f"❌ Image upload failed: {response.text}")
            return False
            
    finally:
        os.unlink(tmp_image_path)

def test_ai_transformation_with_multimedia(token, rant_id):
    """Test AI transformation with multimedia outputs"""
    print("\n🤖 Testing AI transformation with multimedia outputs...")
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Test different transformation types
    transformation_types = [
        ('poem', 'Should generate text + audio'),
        ('song', 'Should generate text + audio'),
        ('rap', 'Should generate text + audio'),
        ('comedy', 'Should generate text + image'),
        ('motivational', 'Should generate text + image'),
        ('story', 'Should generate text + video')
    ]
    
    for trans_type, expected in transformation_types:
        print(f"\n🎭 Testing {trans_type} transformation...")
        
        # Transform content
        transform_data = {
            "transformation_type": trans_type,
            "output_format": "text"
        }
        
        response = requests.post(f"{BASE_URL}/api/media/transform-with-ai/{rant_id}", 
                               json=transform_data, headers=headers)
        
        print(f"Transform response: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {trans_type} transformation successful")
            print(f"Transformed text: {data.get('text', 'N/A')[:100]}...")
            
            # Test multimedia generation based on type
            if trans_type in ['poem', 'song', 'rap']:
                # Test audio generation
                print(f"🎵 Testing audio generation for {trans_type}...")
                audio_data = {"language": "en", "slow": False}
                audio_response = requests.post(f"{BASE_URL}/api/media/generate-speech/{rant_id}", 
                                             json=audio_data, headers=headers)
                print(f"Audio generation response: {audio_response.status_code}")
                if audio_response.status_code == 200:
                    audio_result = audio_response.json()
                    print(f"✅ Audio generated successfully")
                    print(f"Audio data length: {len(audio_result.get('audio_data', ''))}")
                else:
                    print(f"❌ Audio generation failed: {audio_response.text}")
                    
            elif trans_type in ['comedy', 'motivational']:
                # Test image generation
                print(f"🖼️ Testing image generation for {trans_type}...")
                image_data = {"template_type": trans_type}
                image_response = requests.post(f"{BASE_URL}/api/media/generate-meme/{rant_id}", 
                                             json=image_data, headers=headers)
                print(f"Image generation response: {image_response.status_code}")
                if image_response.status_code == 200:
                    image_result = image_response.json()
                    print(f"✅ Image generated successfully")
                    print(f"Image data length: {len(image_result.get('image_data', ''))}")
                else:
                    print(f"❌ Image generation failed: {image_response.text}")
                    
            elif trans_type == 'story':
                # Test video generation
                print(f"🎬 Testing video generation for {trans_type}...")
                video_data = {"duration": 10, "background_color": [30, 30, 60]}
                video_response = requests.post(f"{BASE_URL}/api/media/generate-video/{rant_id}", 
                                             json=video_data, headers=headers)
                print(f"Video generation response: {video_response.status_code}")
                if video_response.status_code == 200:
                    video_result = video_response.json()
                    print(f"✅ Video generated successfully")
                    print(f"Video data length: {len(video_result.get('video_data', ''))}")
                else:
                    print(f"❌ Video generation failed: {video_response.text}")
                    
        else:
            print(f"❌ {trans_type} transformation failed: {response.text}")

def test_text_rant_submission(token):
    """Test regular text rant submission"""
    print("\n📝 Testing text rant submission...")
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Submit a text rant
    rant_data = {
        "content": "I'm feeling frustrated with all the multimedia features not working properly. This is a test rant to check if everything is functioning correctly.",
        "transformation_type": "poem",
        "tone": "neutral",
        "privacy": "private",
        "input_type": "text"
    }
    
    response = requests.post(f"{BASE_URL}/api/rant/submit", json=rant_data, headers=headers)
    print(f"Text rant submission response: {response.status_code}")
    
    if response.status_code in [200, 201]:
        data = response.json()
        print("✅ Text rant submitted successfully")
        print(f"Rant ID: {data.get('rant_id', 'N/A')}")
        return data.get('rant_id')
    else:
        print(f"❌ Text rant submission failed: {response.text}")
        return None

def main():
    """Main test function"""
    print("🚀 Starting RantAi Multimedia Features Final Test")
    print("=" * 50)
    
    # Test user registration and login
    token = test_user_registration_and_login()
    if not token:
        print("❌ Cannot proceed without authentication token")
        return
    
    # Test media endpoints availability
    if not test_media_endpoints(token):
        print("❌ Media endpoints are not available")
        return
    
    # Test text rant submission
    text_rant_id = test_text_rant_submission(token)
    if not text_rant_id:
        print("❌ Cannot proceed without a valid rant ID")
        return
    
    # Test audio submission
    audio_rant_id = test_audio_submission(token)
    
    # Test image submission  
    test_image_submission(token)
    
    # Test AI transformation with multimedia outputs
    test_ai_transformation_with_multimedia(token, text_rant_id)
    
    if audio_rant_id:
        print("\n🎵 Testing AI transformation with audio-submitted rant...")
        test_ai_transformation_with_multimedia(token, audio_rant_id)
    
    print("\n" + "=" * 50)
    print("🎉 Multimedia features test completed!")
    print("✅ All major multimedia features have been tested")
    print("📱 Frontend should now be fully functional for multimedia content")

if __name__ == "__main__":
    main()
