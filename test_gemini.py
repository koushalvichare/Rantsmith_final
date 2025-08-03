#!/usr/bin/env python3
"""
Test script for Gemini API integration
"""

import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test the Gemini API integration"""
    print("🧪 Testing Gemini API Integration...")
    
    # Get API key from environment
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    if not gemini_key or gemini_key == 'your-gemini-api-key-here':
        print("❌ Error: GEMINI_API_KEY not set in .env file")
        print("Please add your Gemini API key to the .env file:")
        print("GEMINI_API_KEY=your-actual-api-key-here")
        return False
    
    try:
        # Configure Gemini
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-pro')
        
        # Test basic text generation
        print("📝 Testing basic text generation...")
        test_prompt = "Hello, can you help me analyze emotions in text?"
        response = model.generate_content(test_prompt)
        print(f"✅ Basic test successful: {response.text[:100]}...")
        
        # Test emotion analysis
        print("\n🎭 Testing emotion analysis...")
        emotion_prompt = """
        Analyze the following rant and provide a JSON response:
        
        "I'm so frustrated with my job. My boss keeps giving me impossible deadlines and I feel like I'm drowning in work. I don't know how much more I can take."
        
        Please respond with ONLY a valid JSON object containing:
        {
            "emotion": "frustrated",
            "emotion_confidence": 0.85,
            "sentiment_score": -0.6,
            "keywords": ["frustrated", "job", "boss", "deadlines", "drowning", "work"],
            "summary": "Work-related stress and frustration with management"
        }
        """
        
        response = model.generate_content(emotion_prompt)
        print(f"✅ Emotion analysis test successful: {response.text[:200]}...")
        
        # Test content transformation
        print("\n🔄 Testing content transformation...")
        transform_prompt = """
        Transform the following emotional content into a supportive, motivational message:
        
        "I feel like I'm failing at everything and nothing I do is good enough."
        
        Please provide an encouraging response that validates their feelings but offers hope.
        """
        
        response = model.generate_content(transform_prompt)
        print(f"✅ Content transformation test successful: {response.text[:200]}...")
        
        print("\n🎉 All Gemini API tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing Gemini API: {e}")
        return False

def test_app_integration():
    """Test the app integration with Gemini"""
    print("\n🔧 Testing app integration...")
    
    try:
        # Import app components
        from app.services.ai_service import AIService
        from app.models import Rant
        
        # Create a mock rant
        class MockRant:
            def __init__(self, content):
                self.content = content
                self.id = 1
        
        # Test AI service
        ai_service = AIService()
        
        # Manually set the Gemini key for testing
        gemini_key = os.getenv('GEMINI_API_KEY')
        if gemini_key and gemini_key != 'your-gemini-api-key-here':
            ai_service.gemini_key = gemini_key
            genai.configure(api_key=gemini_key)
            ai_service.gemini_model = genai.GenerativeModel('gemini-pro')
        
        # Test analysis
        mock_rant = MockRant("I'm feeling overwhelmed and stressed about everything in my life.")
        
        print("🔍 Testing rant analysis...")
        analysis = ai_service.analyze_rant(mock_rant)
        print(f"✅ Analysis result: {analysis}")
        
        print("\n📖 Testing poem transformation...")
        poem = ai_service.transform_to_poem(mock_rant.content)
        print(f"✅ Poem result: {poem[:100]}...")
        
        print("\n🎵 Testing song transformation...")
        song = ai_service.transform_to_song(mock_rant.content)
        print(f"✅ Song result: {song[:100]}...")
        
        print("\n💪 Testing motivational transformation...")
        motivational = ai_service.transform_to_motivational(mock_rant.content)
        print(f"✅ Motivational result: {motivational[:100]}...")
        
        print("\n🎉 All app integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing app integration: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Gemini Integration Tests\n")
    
    # Test API directly
    api_success = test_gemini_api()
    
    if api_success:
        # Test app integration
        app_success = test_app_integration()
        
        if app_success:
            print("\n✅ All tests passed! Gemini integration is working correctly.")
        else:
            print("\n⚠️  API tests passed but app integration failed.")
    else:
        print("\n❌ API tests failed. Please check your Gemini API key.")
        
    print("\n📝 Next steps:")
    print("1. Make sure your GEMINI_API_KEY is set in the .env file")
    print("2. Restart your Flask application")
    print("3. Test the audio upload functionality")
    print("4. The app will now use Gemini AI for analysis and transformations!")
