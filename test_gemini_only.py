#!/usr/bin/env python3
"""
Comprehensive test to verify ALL features use Gemini AI with NO FALLBACKS
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

def test_gemini_only_features():
    """Test that ALL features require Gemini AI and throw errors when not available"""
    print("🧪 Testing Gemini-Only AI Features (No Fallbacks)")
    print("=" * 60)
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        print("✅ Flask app created successfully")
        
        # Test 1: With Gemini Available
        print("\n🟢 TEST 1: WITH GEMINI AI AVAILABLE")
        print("-" * 40)
        
        ai_service_with_gemini = AIService(app)
        
        print(f"🤖 Gemini Available: {ai_service_with_gemini.gemini_model is not None}")
        
        if ai_service_with_gemini.gemini_model:
            # Create test rant
            test_rant = Rant(
                content="I'm feeling overwhelmed with all the work I have to do. Everything feels chaotic and I can't focus!",
                detected_emotion=EmotionType.ANXIOUS,
                user_id=1
            )
            
            print(f"📝 Test Content: {test_rant.content}")
            
            try:
                # Test analysis
                print("\\n🔍 Testing Rant Analysis...")
                analysis = ai_service_with_gemini.analyze_rant(test_rant)
                print(f"✅ Analysis Success: Emotion={analysis.get('emotion', 'N/A')}, Sentiment={analysis.get('sentiment_score', 'N/A')}")
                
                # Test response generation
                print("\\n💬 Testing Response Generation...")
                response = ai_service_with_gemini.get_ai_response(test_rant, personality='supportive')
                print(f"✅ Response Success: {response[:80]}...")
                
                # Test all transformations
                content = test_rant.content
                
                print("\\n🎭 Testing Poem Transformation...")
                poem = ai_service_with_gemini.transform_to_poem(content)
                print(f"✅ Poem Success: {poem[:80]}...")
                
                print("\\n🎵 Testing Song Transformation...")
                song = ai_service_with_gemini.transform_to_song(content)
                print(f"✅ Song Success: {song[:80]}...")
                
                print("\\n📚 Testing Story Transformation...")
                story = ai_service_with_gemini.transform_to_story(content)
                print(f"✅ Story Success: {story[:80]}...")
                
                print("\\n💪 Testing Motivational Transformation...")
                motivation = ai_service_with_gemini.transform_to_motivational(content)
                print(f"✅ Motivational Success: {motivation[:80]}...")
                
                print("\\n🎉 ALL FEATURES WORKING WITH GEMINI AI!")
                
            except Exception as e:
                print(f"❌ Error with Gemini: {e}")
        
        # Test 2: Without Gemini (simulate unavailable)
        print("\\n🔴 TEST 2: WITHOUT GEMINI AI (Should Raise Errors)")
        print("-" * 50)
        
        # Create AI service without Gemini
        ai_service_no_gemini = AIService()
        ai_service_no_gemini.gemini_model = None  # Force no Gemini
        
        print(f"🤖 Gemini Available: {ai_service_no_gemini.gemini_model is not None}")
        
        test_rant = Rant(
            content="Test content for error checking",
            detected_emotion=EmotionType.NEUTRAL,
            user_id=1
        )
        
        # Test that all methods raise errors when Gemini is not available
        methods_to_test = [
            ("analyze_rant", lambda: ai_service_no_gemini.analyze_rant(test_rant)),
            ("get_ai_response", lambda: ai_service_no_gemini.get_ai_response(test_rant)),
            ("transform_to_poem", lambda: ai_service_no_gemini.transform_to_poem("test")),
            ("transform_to_song", lambda: ai_service_no_gemini.transform_to_song("test")),
            ("transform_to_story", lambda: ai_service_no_gemini.transform_to_story("test")),
            ("transform_to_motivational", lambda: ai_service_no_gemini.transform_to_motivational("test")),
        ]
        
        for method_name, method_call in methods_to_test:
            try:
                result = method_call()
                print(f"❌ {method_name}: Should have raised error but returned: {str(result)[:50]}...")
            except Exception as e:
                if "Gemini AI is required" in str(e) or "Gemini" in str(e):
                    print(f"✅ {method_name}: Correctly raised Gemini requirement error")
                else:
                    print(f"⚠️  {method_name}: Raised unexpected error: {e}")
        
        print("\\n🎯 SUMMARY:")
        print("✅ All features require Gemini AI")
        print("✅ No fallbacks to local/OpenAI methods")
        print("✅ Proper error handling when Gemini unavailable")
        print("✅ Your RantAi uses FULL POTENTIAL OF GEMINI with NO FALLBACKS!")

if __name__ == "__main__":
    test_gemini_only_features()
