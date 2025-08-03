import google.generativeai as genai
import json
import os
from typing import Dict, Any, Optional
from flask import current_app
from app.models import Rant, EmotionType

class GeminiService:
    """AI service using Google's Gemini API for processing rants and generating insights"""
    
    def __init__(self, app=None):
        self.app = app
        self.gemini_key = None
        self.model = None
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with Flask app"""
        self.app = app
        with app.app_context():
            self.gemini_key = app.config.get('GEMINI_API_KEY')
            if self.gemini_key:
                genai.configure(api_key=self.gemini_key)
                self.model = genai.GenerativeModel('gemini-pro')
    
    def analyze_rant(self, rant: Rant) -> Dict[str, Any]:
        """Analyze a rant for emotion, sentiment, and keywords"""
        try:
            if self.model and self.gemini_key:
                return self._analyze_with_gemini(rant)
            else:
                return self._analyze_with_fallback(rant)
        except Exception as e:
            print(f"Error analyzing rant with Gemini: {e}")
            return self._analyze_with_fallback(rant)
    
    def _analyze_with_gemini(self, rant: Rant) -> Dict[str, Any]:
        """Analyze rant using Gemini API"""
        prompt = f"""
        Analyze the following rant and provide a detailed emotional and sentiment analysis.
        
        Rant: "{rant.content}"
        
        Please respond with ONLY a valid JSON object containing:
        {{
            "emotion": "one of: angry, frustrated, sad, anxious, excited, happy, confused, neutral",
            "emotion_confidence": 0.85,
            "sentiment_score": -0.3,
            "keywords": ["word1", "word2", "word3"],
            "summary": "Brief summary of the main issue or topic",
            "intensity": 0.7,
            "categories": ["category1", "category2"]
        }}
        
        Make sure emotion_confidence and sentiment_score are numbers between 0-1 and -1 to 1 respectively.
        Intensity should be 0-1 representing how intense the emotion is.
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Try to extract JSON from the response
            if response_text.startswith('```json'):
                response_text = response_text[7:-3]
            elif response_text.startswith('```'):
                response_text = response_text[3:-3]
            
            analysis = json.loads(response_text)
            
            # Validate the response structure
            required_fields = ['emotion', 'emotion_confidence', 'sentiment_score', 'keywords', 'summary']
            for field in required_fields:
                if field not in analysis:
                    raise ValueError(f"Missing required field: {field}")
            
            return {
                'emotion': analysis.get('emotion', 'neutral'),
                'emotion_confidence': float(analysis.get('emotion_confidence', 0.5)),
                'sentiment_score': float(analysis.get('sentiment_score', 0.0)),
                'keywords': analysis.get('keywords', []),
                'summary': analysis.get('summary', 'No summary available'),
                'intensity': float(analysis.get('intensity', 0.5)),
                'categories': analysis.get('categories', [])
            }
            
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            print(f"Error parsing Gemini response: {e}")
            return self._analyze_with_fallback(rant)
    
    def _analyze_with_fallback(self, rant: Rant) -> Dict[str, Any]:
        """Fallback analysis when Gemini is not available"""
        content = rant.content.lower()
        
        # Simple keyword-based emotion detection
        emotion_keywords = {
            'angry': ['angry', 'mad', 'furious', 'rage', 'hate', 'stupid', 'damn', 'hell'],
            'frustrated': ['frustrated', 'annoying', 'irritated', 'bothered', 'fed up'],
            'sad': ['sad', 'depressed', 'down', 'upset', 'cry', 'hurt', 'broken'],
            'anxious': ['anxious', 'worried', 'nervous', 'scared', 'fear', 'panic'],
            'excited': ['excited', 'amazing', 'awesome', 'great', 'love', 'wonderful'],
            'happy': ['happy', 'glad', 'joy', 'smile', 'laugh', 'good', 'nice'],
            'confused': ['confused', 'lost', 'unclear', 'wondering', 'puzzled']
        }
        
        detected_emotion = 'neutral'
        max_matches = 0
        
        for emotion, keywords in emotion_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in content)
            if matches > max_matches:
                max_matches = matches
                detected_emotion = emotion
        
        # Simple sentiment analysis
        positive_words = ['good', 'great', 'awesome', 'amazing', 'love', 'happy', 'wonderful']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'angry', 'sad', 'frustrated']
        
        pos_count = sum(1 for word in positive_words if word in content)
        neg_count = sum(1 for word in negative_words if word in content)
        
        if pos_count + neg_count == 0:
            sentiment_score = 0.0
        else:
            sentiment_score = (pos_count - neg_count) / (pos_count + neg_count)
        
        # Extract simple keywords
        words = content.split()
        keywords = [word for word in words if len(word) > 3][:5]
        
        return {
            'emotion': detected_emotion,
            'emotion_confidence': min(max_matches / 3, 1.0),
            'sentiment_score': sentiment_score,
            'keywords': keywords,
            'summary': f"Content focuses on {detected_emotion} feelings",
            'intensity': min(max_matches / 2, 1.0),
            'categories': ['personal', 'emotional']
        }
    
    def generate_response(self, rant: Rant, response_type: str = "supportive") -> str:
        """Generate a supportive response to a rant"""
        try:
            if self.model and self.gemini_key:
                return self._generate_response_with_gemini(rant, response_type)
            else:
                return self._generate_response_fallback(rant, response_type)
        except Exception as e:
            print(f"Error generating response with Gemini: {e}")
            return self._generate_response_fallback(rant, response_type)
    
    def _generate_response_with_gemini(self, rant: Rant, response_type: str) -> str:
        """Generate response using Gemini API"""
        prompt = f"""
        Generate a {response_type} response to this rant. The response should be empathetic, 
        understanding, and provide gentle guidance or validation.
        
        Rant: "{rant.content}"
        
        Response type: {response_type}
        
        Please provide a thoughtful, caring response that:
        1. Acknowledges their feelings
        2. Validates their experience
        3. Offers gentle perspective or encouragement
        4. Keeps it conversational and supportive
        
        Response:
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating Gemini response: {e}")
            return self._generate_response_fallback(rant, response_type)
    
    def _generate_response_fallback(self, rant: Rant, response_type: str) -> str:
        """Fallback response generation"""
        responses = {
            'supportive': "I hear you, and your feelings are completely valid. It sounds like you're going through a challenging time, and that's okay. Remember that it's normal to feel this way, and you're not alone in experiencing these emotions.",
            'encouraging': "Your feelings matter, and it's brave of you to express them. Every challenge you face is helping you grow stronger, even when it doesn't feel that way. You have the strength to get through this.",
            'analytical': "It seems like this situation is really affecting you. Sometimes it helps to break down what's happening and look at it from different angles. What do you think might be the root cause of these feelings?",
            'empathetic': "I can really feel the emotion in your words. It must be difficult to be experiencing this right now. Know that your feelings are heard and understood."
        }
        
        return responses.get(response_type, responses['supportive'])
    
    def transform_content(self, content: str, transformation_type: str) -> str:
        """Transform rant content into different formats"""
        try:
            if self.model and self.gemini_key:
                return self._transform_with_gemini(content, transformation_type)
            else:
                return self._transform_with_fallback(content, transformation_type)
        except Exception as e:
            print(f"Error transforming content with Gemini: {e}")
            return self._transform_with_fallback(content, transformation_type)
    
    def _transform_with_gemini(self, content: str, transformation_type: str) -> str:
        """Transform content using Gemini API"""
        prompts = {
            'poem': f"Transform this emotional content into a meaningful poem that captures the essence of the feelings expressed:\n\n{content}",
            'song': f"Transform this content into song lyrics with verses and a chorus:\n\n{content}",
            'story': f"Transform this emotional content into a short, uplifting story:\n\n{content}",
            'motivational': f"Transform this content into an inspiring, motivational message:\n\n{content}",
            'letter': f"Transform this content into a supportive letter to oneself:\n\n{content}"
        }
        
        prompt = prompts.get(transformation_type, prompts['motivational'])
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error transforming with Gemini: {e}")
            return self._transform_with_fallback(content, transformation_type)
    
    def _transform_with_fallback(self, content: str, transformation_type: str) -> str:
        """Fallback content transformation"""
        transformations = {
            'poem': f"In feelings deep and true,\n{content[:100]}...\nThrough darkness comes the light,\nAnd hope will see us through.",
            'song': f"[Verse 1]\n{content[:150]}...\n\n[Chorus]\nEvery feeling has its place\nIn this journey that we face\nThrough the storms we find our way\nTo a brighter, better day",
            'story': f"Once there was someone who felt just like this: {content[:200]}... And through understanding their emotions, they found strength they never knew they had.",
            'motivational': f"Your feelings are valid and important. {content[:100]}... Remember: you are stronger than you know, and this moment is part of your growth story.",
            'letter': f"Dear Self,\n\nI want you to know that what you're feeling is completely normal and valid. {content[:150]}... You are worthy of love, understanding, and patience - especially from yourself.\n\nWith compassion,\nYour Inner Supporter"
        }
        
        return transformations.get(transformation_type, transformations['motivational'])
    
    def get_insight(self, rant: Rant) -> str:
        """Get AI-generated insight about a rant"""
        try:
            if self.model and self.gemini_key:
                return self._get_insight_with_gemini(rant)
            else:
                return self._get_insight_fallback(rant)
        except Exception as e:
            print(f"Error getting insight with Gemini: {e}")
            return self._get_insight_fallback(rant)
    
    def _get_insight_with_gemini(self, rant: Rant) -> str:
        """Get insight using Gemini API"""
        prompt = f"""
        Provide a gentle, insightful reflection on this person's emotional expression. 
        Focus on patterns, potential growth opportunities, and affirming observations.
        
        Content: "{rant.content}"
        
        Please provide a thoughtful insight that:
        1. Reflects on what this expression reveals about their emotional state
        2. Identifies any patterns or themes
        3. Offers a perspective that might be helpful
        4. Remains supportive and non-judgmental
        
        Insight:
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error getting Gemini insight: {e}")
            return self._get_insight_fallback(rant)
    
    def _get_insight_fallback(self, rant: Rant) -> str:
        """Fallback insight generation"""
        return f"This expression shows a lot of emotional depth and self-awareness. The fact that you're putting these feelings into words is actually a healthy way of processing what you're experiencing. Your emotions are giving you important information about what matters to you."
