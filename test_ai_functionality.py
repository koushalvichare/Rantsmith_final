#!/usr/bin/env python3
"""
Test script to verify AI functionality is working properly
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.services.ai_service import AIService
from app.models import Rant, EmotionType

def test_ai_service():
    """Test the AI service functionality"""
    print("🧪 Testing AI Service Functionality...")
    print("=" * 50)
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        # Initialize AI service with app context
        ai_service = AIService(app)  # Pass app to constructor
        
        print(f"🤖 Gemini Model Available: {ai_service.gemini_model is not None}")
        print(f"🤖 OpenAI Available: {hasattr(ai_service, 'openai_key') and ai_service.openai_key}")
        print(f"🔑 Gemini Key: {'✅ Set' if ai_service.gemini_key else '❌ Not Set'}")
        print(f"🔑 OpenAI Key: {'✅ Set' if ai_service.openai_key else '❌ Not Set'}")
        print(f"🌐 Environment GEMINI_API_KEY: {'✅ Set' if os.getenv('GEMINI_API_KEY') else '❌ Not Set'}")
        
        # Create a test rant
        test_rant = Rant(
            content="I'm so frustrated with work today! My boss keeps giving me impossible deadlines and I feel completely overwhelmed.",
            detected_emotion=EmotionType.FRUSTRATED,
            user_id=1  # Add required user_id
        )
        
        print(f"\n📝 Test Rant: {test_rant.content}")
        print("-" * 50)
        
        try:
            # Test analysis
            print("🔍 Testing Rant Analysis...")
            analysis = ai_service.analyze_rant(test_rant)
            print(f"✅ Analysis Result:")
            print(f"   Emotion: {analysis.get('emotion', 'N/A')}")
            print(f"   Sentiment: {analysis.get('sentiment_score', 'N/A')}")
            print(f"   Summary: {analysis.get('summary', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Analysis Error: {e}")
        
        try:
            # Test response generation
            print("\n💬 Testing Response Generation...")
            response = ai_service.get_ai_response(test_rant, personality='supportive')
            print(f"✅ Response Generated: {response[:100]}...")
            
        except Exception as e:
            print(f"❌ Response Error: {e}")
        
        try:
            # Test poem transformation
            print("\n🎭 Testing Poem Transformation...")
            poem = ai_service.transform_to_poem(test_rant.content)
            print(f"✅ Poem Created: {poem[:100]}...")
            
        except Exception as e:
            print(f"❌ Poem Error: {e}")
        
        try:
            # Test song transformation
            print("\n🎵 Testing Song Transformation...")
            song = ai_service.transform_to_song(test_rant.content)
            print(f"✅ Song Created: {song[:100]}...")
            
        except Exception as e:
            print(f"❌ Song Error: {e}")

if __name__ == "__main__":
    test_ai_service()
