#!/usr/bin/env python3
"""
Test multimedia features specifically
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_multimedia_features():
    """Test multimedia generation features"""
    print("🎬 Testing Multimedia Features")
    print("=" * 40)
    
    # First login to get token
    try:
        login_data = {
            "email": "test123@example.com",
            "password": "testpass123"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code != 200:
            print("❌ Login failed")
            return False
        
        token = response.json().get('token')
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        
        # Create a test rant
        rant_data = {
            "content": "I'm feeling excited about testing all these multimedia features! This should generate audio, images, and videos!",
            "transformation_type": "song",
            "tone": "positive",
            "privacy": "private",
            "input_type": "text"
        }
        
        rant_response = requests.post(f"{BASE_URL}/api/rant/submit", json=rant_data, headers=headers)
        if rant_response.status_code not in [200, 201]:
            print("❌ Rant submission failed")
            return False
            
        rant_id = rant_response.json().get('rant_id')
        print(f"✅ Created rant ID: {rant_id}")
        
        # Test text transformation
        transform_response = requests.post(f"{BASE_URL}/api/media/transform-with-ai/{rant_id}", 
                                         json={"transformation_type": "song", "output_format": "text"}, 
                                         headers=headers)
        if transform_response.status_code == 200:
            print("✅ Text transformation working")
        else:
            print(f"❌ Text transformation failed: {transform_response.status_code}")
        
        # Test audio generation
        audio_response = requests.post(f"{BASE_URL}/api/media/generate-speech/{rant_id}", 
                                     json={"language": "en", "slow": False}, 
                                     headers=headers)
        if audio_response.status_code == 200:
            print("✅ Audio generation working")
        else:
            print(f"❌ Audio generation failed: {audio_response.status_code}")
        
        # Test image generation
        image_response = requests.post(f"{BASE_URL}/api/media/generate-meme/{rant_id}", 
                                     json={"template_type": "motivational"}, 
                                     headers=headers)
        if image_response.status_code == 200:
            print("✅ Image generation working")
        else:
            print(f"❌ Image generation failed: {image_response.status_code}")
        
        # Test video generation
        video_response = requests.post(f"{BASE_URL}/api/media/generate-video/{rant_id}", 
                                     json={"duration": 10, "background_color": [30, 30, 60]}, 
                                     headers=headers)
        if video_response.status_code == 200:
            print("✅ Video generation working")
        else:
            print(f"❌ Video generation failed: {video_response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_multimedia_features()
