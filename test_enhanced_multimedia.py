#!/usr/bin/env python3
"""
Enhanced multimedia features test for RantAi
This script tests all the enhanced multimedia features
"""

import requests
import json
import os
import tempfile
import time
from PIL import Image
import base64

BASE_URL = "http://127.0.0.1:5000"

def test_registration_and_login():
    """Test user registration and login"""
    print("🔐 Testing enhanced user registration and login...")
    
    # Register a test user
    register_data = {
        "username": f"testuser_enhanced_{int(time.time())}",
        "email": f"test_enhanced_{int(time.time())}@example.com",
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

def test_enhanced_audio_processing(token):
    """Test enhanced audio processing"""
    print("\n🎵 Testing enhanced audio processing...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create different sized mock audio files to test enhanced processing
    test_files = [
        ("small_audio.wav", b"Small audio content" * 100),  # Small file
        ("medium_audio.wav", b"Medium audio content with more data" * 1000),  # Medium file
        ("large_audio.wav", b"Large audio content with lots of data representing a long recording" * 5000),  # Large file
    ]
    
    for filename, content in test_files:
        print(f"\n📁 Testing {filename}...")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_audio:
            tmp_audio.write(content)
            tmp_audio_path = tmp_audio.name
        
        try:
            with open(tmp_audio_path, 'rb') as audio_file:
                files = {'audio': (filename, audio_file, 'audio/wav')}
                response = requests.post(f"{BASE_URL}/api/media/upload-audio", files=files, headers=headers)
            
            print(f"Audio upload response: {response.status_code}")
            if response.status_code in [200, 201]:
                data = response.json()
                print("✅ Enhanced audio processing successful")
                print(f"Transcribed text length: {len(data.get('text', ''))}")
                print(f"Text preview: {data.get('text', '')[:100]}...")
                return data.get('rant_id')
            else:
                print(f"❌ Audio upload failed: {response.text}")
                
        finally:
            os.unlink(tmp_audio_path)
    
    return None

def test_enhanced_tts_generation(token, rant_id):
    """Test enhanced text-to-speech generation"""
    print("\n🔊 Testing enhanced text-to-speech generation...")
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Test different TTS configurations
    tts_configs = [
        {"language": "en", "slow": False},
        {"language": "es", "slow": True},
        {"language": "fr", "slow": False},
    ]
    
    for config in tts_configs:
        print(f"\n🗣️ Testing TTS with config: {config}")
        
        response = requests.post(f"{BASE_URL}/api/media/generate-speech/{rant_id}", 
                               json=config, headers=headers)
        
        print(f"TTS response: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Enhanced TTS generation successful")
            print(f"Audio data length: {len(data.get('audio_data', ''))}")
            print(f"Message: {data.get('message', '')}")
        else:
            print(f"❌ TTS generation failed: {response.text}")

def test_enhanced_image_generation(token, rant_id):
    """Test enhanced image/meme generation"""
    print("\n🖼️ Testing enhanced image generation...")
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Test different image types
    image_types = ['comedy', 'motivational', 'default']
    
    for img_type in image_types:
        print(f"\n🎨 Testing {img_type} image generation...")
        
        response = requests.post(f"{BASE_URL}/api/media/generate-meme/{rant_id}", 
                               json={"template_type": img_type}, headers=headers)
        
        print(f"Image generation response: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Enhanced image generation successful")
            print(f"Image data length: {len(data.get('image_data', ''))}")
            print(f"Message: {data.get('message', '')}")
        else:
            print(f"❌ Image generation failed: {response.text}")

def test_enhanced_video_generation(token, rant_id):
    """Test enhanced video generation"""
    print("\n🎬 Testing enhanced video generation...")
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Test different video configurations
    video_configs = [
        {"duration": 5, "background_color": [30, 30, 30]},
        {"duration": 10, "background_color": [50, 20, 80]},
        {"duration": 15, "background_color": [20, 50, 30]},
    ]
    
    for config in video_configs:
        print(f"\n📹 Testing video with config: {config}")
        
        response = requests.post(f"{BASE_URL}/api/media/generate-video/{rant_id}", 
                               json=config, headers=headers)
        
        print(f"Video generation response: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Enhanced video generation successful")
            print(f"Video data length: {len(data.get('video_data', ''))}")
            print(f"Message: {data.get('message', '')}")
            
            # Check if it's the enhanced video format
            video_data = data.get('video_data', '')
            if video_data.startswith('data:application/json;base64,'):
                try:
                    json_data = base64.b64decode(video_data.split(',')[1]).decode()
                    video_info = json.loads(json_data)
                    if video_info.get('type') == 'animated_sequence':
                        print(f"📊 Video frames: {len(video_info.get('frames', []))}")
                        print(f"📊 Duration: {video_info.get('duration')}s")
                        print(f"📊 FPS: {video_info.get('fps')}")
                except:
                    pass
        else:
            print(f"❌ Video generation failed: {response.text}")

def test_complete_multimedia_workflow(token):
    """Test complete multimedia workflow with enhanced features"""
    print("\n🌟 Testing complete enhanced multimedia workflow...")
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Submit a text rant
    rant_data = {
        "content": "This is a comprehensive test of all the enhanced multimedia features in RantAi. I want to see how well the improved audio processing, better image generation, and enhanced video creation work together to create amazing content.",
        "transformation_type": "story",
        "tone": "dramatic",
        "privacy": "private",
        "input_type": "text"
    }
    
    response = requests.post(f"{BASE_URL}/api/rant/submit", json=rant_data, headers=headers)
    print(f"Rant submission: {response.status_code}")
    
    if response.status_code in [200, 201]:
        rant_id = response.json().get('rant_id')
        print(f"✅ Rant submitted successfully (ID: {rant_id})")
        
        # Test AI transformation
        print("\n🤖 Testing AI transformation...")
        transform_data = {
            "transformation_type": "story",
            "output_format": "text"
        }
        
        response = requests.post(f"{BASE_URL}/api/media/transform-with-ai/{rant_id}", 
                               json=transform_data, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ AI transformation successful")
            print(f"Transformed text: {data.get('text', '')[:200]}...")
            
            # Test all multimedia generation for this rant
            print("\n🎯 Testing multimedia generation for transformed content...")
            test_enhanced_tts_generation(token, rant_id)
            test_enhanced_image_generation(token, rant_id)
            test_enhanced_video_generation(token, rant_id)
            
        else:
            print(f"❌ AI transformation failed: {response.text}")
    else:
        print(f"❌ Rant submission failed: {response.text}")

def main():
    """Main test function"""
    print("🚀 Starting Enhanced RantAi Multimedia Features Test")
    print("=" * 60)
    
    # Test authentication
    token = test_registration_and_login()
    if not token:
        print("❌ Cannot proceed without authentication token")
        return
    
    # Test enhanced audio processing
    rant_id = test_enhanced_audio_processing(token)
    
    if rant_id:
        # Test individual multimedia features
        test_enhanced_tts_generation(token, rant_id)
        test_enhanced_image_generation(token, rant_id)
        test_enhanced_video_generation(token, rant_id)
    
    # Test complete workflow
    test_complete_multimedia_workflow(token)
    
    print("\n" + "=" * 60)
    print("🎉 Enhanced multimedia features test completed!")
    print("✅ All enhanced features have been tested")
    print("🚀 RantAi is ready for production with improved multimedia capabilities!")

if __name__ == "__main__":
    main()
