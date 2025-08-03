#!/usr/bin/env python3
"""
End-to-End Test Suite for RantAi Production Readiness
Tests the complete user workflow from registration to content generation
"""

import requests
import json
import time
import os
from pathlib import Path
import tempfile
import wave
import numpy as np

BASE_URL = "http://127.0.0.1:5000"
FRONTEND_URL = "http://localhost:3004"

class RantAiE2ETest:
    def __init__(self):
        self.token = None
        self.user_id = None
        self.rant_id = None
        self.results = []
        
    def log_result(self, test_name, success, message=""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.results.append({
            'test': test_name,
            'status': status,
            'message': message
        })
        print(f"{status}: {test_name}")
        if message:
            print(f"   {message}")
    
    def create_test_user(self):
        """Create a test user account"""
        try:
            # Generate unique test user
            timestamp = str(int(time.time()))
            test_user = {
                "username": f"e2e_test_{timestamp}",
                "email": f"e2e_test_{timestamp}@test.com",
                "password": "TestPass123!"
            }
            
            # Register user
            response = requests.post(f"{BASE_URL}/auth/register", json=test_user)
            if response.status_code in [200, 201]:
                self.log_result("User Registration", True, f"User created: {test_user['email']}")
                
                # Login immediately
                login_response = requests.post(f"{BASE_URL}/auth/login", json={
                    "email": test_user["email"],
                    "password": test_user["password"]
                })
                
                if login_response.status_code == 200:
                    login_data = login_response.json()
                    self.token = login_data.get('token')
                    self.user_id = login_data.get('user', {}).get('id')
                    self.log_result("User Login", True, f"Token received: {self.token[:20]}...")
                    return True
                else:
                    self.log_result("User Login", False, f"Login failed: {login_response.status_code}")
                    return False
            else:
                self.log_result("User Registration", False, f"Registration failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("User Registration", False, f"Exception: {str(e)}")
            return False
    
    def test_text_rant_submission(self):
        """Test submitting a text rant"""
        try:
            headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
            
            rant_data = {
                "content": "This is an end-to-end test rant. I'm testing the complete workflow of RantAi including text submission, AI processing, and content transformation. This should work seamlessly!",
                "transformation_type": "poem",
                "tone": "optimistic",
                "privacy": "private",
                "input_type": "text"
            }
            
            response = requests.post(f"{BASE_URL}/api/rant/submit", json=rant_data, headers=headers)
            if response.status_code in [200, 201]:
                data = response.json()
                self.rant_id = data.get('rant_id')
                self.log_result("Text Rant Submission", True, f"Rant ID: {self.rant_id}")
                return True
            else:
                self.log_result("Text Rant Submission", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Text Rant Submission", False, f"Exception: {str(e)}")
            return False
    
    def test_ai_transformation(self):
        """Test AI transformation of the rant"""
        try:
            if not self.rant_id:
                self.log_result("AI Transformation", False, "No rant ID available")
                return False
                
            headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
            
            transform_data = {
                "transformation_type": "poem",
                "output_format": "text"
            }
            
            response = requests.post(f"{BASE_URL}/api/media/transform-with-ai/{self.rant_id}", json=transform_data, headers=headers)
            if response.status_code == 200:
                data = response.json()
                transformed_text = data.get('text', '')
                self.log_result("AI Transformation", True, f"Transformed text length: {len(transformed_text)} characters")
                return True
            else:
                self.log_result("AI Transformation", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("AI Transformation", False, f"Exception: {str(e)}")
            return False
    
    def create_test_audio(self):
        """Create a test audio file"""
        try:
            # Create a simple audio file (sine wave)
            duration = 2  # seconds
            sample_rate = 44100
            frequency = 440  # A4 note
            
            # Generate sine wave
            t = np.linspace(0, duration, int(sample_rate * duration))
            audio_data = np.sin(2 * np.pi * frequency * t)
            
            # Convert to 16-bit PCM
            audio_data = (audio_data * 32767).astype(np.int16)
            
            # Create temporary WAV file
            temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            with wave.open(temp_file.name, 'wb') as wav_file:
                wav_file.setnchannels(1)  # mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio_data.tobytes())
            
            return temp_file.name
            
        except Exception as e:
            self.log_result("Audio File Creation", False, f"Exception: {str(e)}")
            return None
    
    def test_audio_upload(self):
        """Test audio file upload"""
        try:
            audio_file_path = self.create_test_audio()
            if not audio_file_path:
                return False
                
            headers = {"Authorization": f"Bearer {self.token}"}
            
            with open(audio_file_path, 'rb') as audio_file:
                files = {"audio": ("test_audio.wav", audio_file, "audio/wav")}
                response = requests.post(f"{BASE_URL}/api/media/upload-audio", files=files, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    transcribed_text = data.get('text', '')
                    self.log_result("Audio Upload", True, f"Transcribed text: {transcribed_text[:50]}...")
                    cleanup_success = True
                else:
                    self.log_result("Audio Upload", False, f"Status: {response.status_code}, Response: {response.text}")
                    cleanup_success = False
            
            # Clean up temporary file
            try:
                os.unlink(audio_file_path)
            except:
                pass
                
            return cleanup_success
            
        except Exception as e:
            self.log_result("Audio Upload", False, f"Exception: {str(e)}")
            return False
    
    def test_image_upload(self):
        """Test image file upload"""
        try:
            # Create a simple test image (1x1 pixel PNG)
            import io
            from PIL import Image
            
            # Create a small red image
            img = Image.new('RGB', (10, 10), color='red')
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            headers = {"Authorization": f"Bearer {self.token}"}
            files = {"image": ("test_image.png", img_bytes, "image/png")}
            
            response = requests.post(f"{BASE_URL}/api/media/upload-image", files=files, headers=headers)
            if response.status_code == 200:
                data = response.json()
                self.log_result("Image Upload", True, f"Image processed: {data.get('message', 'Success')}")
                return True
            else:
                self.log_result("Image Upload", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Image Upload", False, f"Exception: {str(e)}")
            # Try without PIL as fallback
            try:
                # Create simple bytes for testing
                fake_image = b'\x89PNG\r\n\x1a\n' + b'\x00' * 100  # Fake PNG header + data
                headers = {"Authorization": f"Bearer {self.token}"}
                files = {"image": ("test_image.png", fake_image, "image/png")}
                
                response = requests.post(f"{BASE_URL}/api/media/upload-image", files=files, headers=headers)
                if response.status_code == 200:
                    self.log_result("Image Upload (Fallback)", True, "Basic image upload test passed")
                    return True
                else:
                    self.log_result("Image Upload (Fallback)", False, f"Status: {response.status_code}")
                    return False
            except Exception as e2:
                self.log_result("Image Upload", False, f"Fallback also failed: {str(e2)}")
                return False
    
    def test_multiple_transformations(self):
        """Test multiple AI transformation types"""
        if not self.rant_id:
            self.log_result("Multiple Transformations", False, "No rant ID available")
            return False
            
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        transformations = ['poem', 'song', 'story', 'motivational']
        success_count = 0
        
        for transformation in transformations:
            try:
                transform_data = {
                    "transformation_type": transformation,
                    "output_format": "text"
                }
                
                response = requests.post(f"{BASE_URL}/api/media/transform-with-ai/{self.rant_id}", json=transform_data, headers=headers)
                if response.status_code == 200:
                    success_count += 1
                    self.log_result(f"AI Transform ({transformation})", True, f"Successfully transformed to {transformation}")
                else:
                    self.log_result(f"AI Transform ({transformation})", False, f"Status: {response.status_code}")
                    
            except Exception as e:
                self.log_result(f"AI Transform ({transformation})", False, f"Exception: {str(e)}")
        
        overall_success = success_count >= 2  # At least 2 out of 4 should work
        self.log_result("Multiple Transformations", overall_success, f"{success_count}/{len(transformations)} transformations succeeded")
        return overall_success
    
    def run_complete_test_suite(self):
        """Run the complete end-to-end test suite"""
        print("🚀 Starting End-to-End Test Suite for RantAi")
        print("=" * 50)
        
        # Test user creation and authentication
        if not self.create_test_user():
            print("❌ User creation failed - stopping tests")
            return False
        
        # Test core functionality
        self.test_text_rant_submission()
        self.test_ai_transformation()
        self.test_audio_upload()
        self.test_image_upload()
        self.test_multiple_transformations()
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 Test Summary")
        print("=" * 50)
        
        passed = sum(1 for r in self.results if "✅ PASS" in r['status'])
        failed = sum(1 for r in self.results if "❌ FAIL" in r['status'])
        
        for result in self.results:
            print(f"{result['status']}: {result['test']}")
        
        print(f"\n📈 Results: {passed} passed, {failed} failed")
        
        if failed == 0:
            print("🎉 ALL TESTS PASSED! RantAi is ready for production! 🚀")
            return True
        else:
            print(f"⚠️  {failed} test(s) failed. Review issues before production deployment.")
            return False

def main():
    """Main function to run the test suite"""
    tester = RantAiE2ETest()
    success = tester.run_complete_test_suite()
    
    if success:
        print("\n✅ RantAi is production-ready!")
        print("🔧 Next steps:")
        print("   1. Deploy to production environment")
        print("   2. Configure production database")
        print("   3. Set up monitoring and logging")
        print("   4. Update environment variables")
        print("   5. Configure SSL certificates")
    else:
        print("\n❌ Some tests failed. Address issues before production deployment.")
    
    return success

if __name__ == "__main__":
    main()
