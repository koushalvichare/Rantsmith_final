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
        self.generation_configs = {}
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with Flask app and configure Gemini"""
        self.app = app
        with app.app_context():
            self.gemini_key = app.config.get('GEMINI_API_KEY')
            if self.gemini_key:
                try:
                    genai.configure(api_key=self.gemini_key)
                    # Use flash model for higher quota limits
                    self.model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # Define different generation configs for different tasks
                    self.generation_configs = {
                        'analysis': genai.types.GenerationConfig(
                            temperature=0.1,
                            top_p=0.95,
                            top_k=40,
                            max_output_tokens=1024
                        ),
                        'creative': genai.types.GenerationConfig(
                            temperature=0.95,  # Even higher for maximum creativity and variety
                            top_p=0.9,
                            top_k=60,  # More diversity in word choice
                            max_output_tokens=2048,
                        ),
                        'insightful': genai.types.GenerationConfig(
                            temperature=0.6,
                            top_p=0.95,
                            top_k=40,
                            max_output_tokens=2048,
                        )
                    }
                    print("✅ Gemini Service initialized successfully with gemini-1.5-flash.")
                except Exception as e:
                    print(f"❌ Error initializing Gemini Service: {e}")
                    self.model = None
    
    def analyze_rant(self, rant: Rant) -> Dict[str, Any]:
        """Analyze a rant for emotion, sentiment, and keywords"""
        if self.model:
            return self._analyze_with_gemini(rant)
        return self._analyze_with_fallback(rant)
    
    def _analyze_with_gemini(self, rant: Rant) -> Dict[str, Any]:
        """Analyze rant using Gemini API with optimized settings"""
        prompt = f"""
        Analyze the following rant and provide a detailed emotional and sentiment analysis.
        
        Rant: "{rant.content}"
        
        Respond with ONLY a valid JSON object with the following schema:
        {{
            "emotion": "one of: angry, frustrated, sad, anxious, excited, happy, confused, neutral",
            "emotion_confidence": float,
            "sentiment_score": float,
            "keywords": ["string"],
            "summary": "string",
            "intensity": float,
            "categories": ["string"]
        }}
        
        Ensure emotion_confidence is 0.0-1.0, sentiment_score is -1.0-1.0, and intensity is 0.0-1.0.
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_configs.get('analysis')
            )
            analysis = json.loads(response.text)
            
            # Validate and format the response
            required_fields = ['emotion', 'emotion_confidence', 'sentiment_score', 'keywords', 'summary']
            if not all(field in analysis for field in required_fields):
                raise ValueError("Missing one or more required fields in Gemini response.")

            return {
                'emotion': analysis.get('emotion', 'neutral'),
                'emotion_confidence': float(analysis.get('emotion_confidence', 0.5)),
                'sentiment_score': float(analysis.get('sentiment_score', 0.0)),
                'keywords': analysis.get('keywords', []),
                'summary': analysis.get('summary', 'No summary available.'),
                'intensity': float(analysis.get('intensity', 0.5)),
                'categories': analysis.get('categories', [])
            }
            
        except (json.JSONDecodeError, ValueError, KeyError, Exception) as e:
            print(f"Error processing Gemini analysis response: {e}")
            return self._analyze_with_fallback(rant)

    def generate_response(self, rant: Rant, response_type: str = "supportive") -> str:
        """Generate a supportive response to a rant"""
        print(f"🔍 Gemini service - API key present: {bool(self.gemini_key)}")
        print(f"🔍 Gemini service - Model available: {bool(self.model)}")
        if self.model:
            return self._generate_response_with_gemini(rant, response_type)
        return self._generate_response_fallback(rant, response_type)

    def _generate_response_with_gemini(self, rant: Rant, response_type: str) -> str:
        """Generate response using Gemini API with creative settings"""
        user_message = rant.content.strip()
        
        # Define detailed personality prompts for more specific and creative responses
        personality_prompts = {
            'psychologist': f"""
You are Dr. Sarah, a warm and exceptionally caring psychologist who specializes in uplifting people's moods and helping them feel better about themselves. You have a unique gift for making people feel heard, validated, and emotionally supported. You focus on emotional healing and mood enhancement rather than clinical analysis.

Your approach:
- FIRST acknowledge and validate their emotions with genuine empathy
- Provide immediate emotional comfort and reassurance
- Offer uplifting perspectives and hope
- Share gentle wisdom that makes them feel better about themselves
- Use warm, encouraging language that lifts their spirits
- Focus on their strengths and resilience
- If they want a joke, tell genuinely funny, mood-lifting jokes
- Always end with something that makes them feel valued and supported

IMPORTANT: Your primary goal is to make the user feel emotionally better and more positive. Be genuinely caring, not clinical.

User's message: "{user_message}"

Respond as Dr. Sarah would - prioritizing emotional support, validation, and mood uplift above all else.
""",
            'supportive': f"""
You are Alex, the most emotionally supportive and uplifting best friend anyone could ask for. You have an extraordinary gift for making people feel deeply loved, understood, and valued exactly as they are. Your presence alone makes people feel better.

Your style:
- Immediately validate their feelings with genuine warmth
- Make them feel heard and understood on a deep level
- Share the emotional load by expressing genuine empathy
- Offer comfort that feels like a warm, supportive hug
- Help them see their own worth and strength
- Use language that makes them feel less alone
- Provide emotional safety and unconditional acceptance
- Always remind them how much they matter

User's message: "{user_message}"

Respond as Alex would - with pure emotional support, validation, and the kind of love that heals.
""",
            'humorous': f"""
You are Charlie, a naturally funny and uplifting comedian-therapist who has mastered the art of using humor to genuinely make people feel better. You have perfect timing, emotional intelligence, and the rare ability to make people laugh while feeling truly supported.

Your style:
- Tell actually funny, original jokes that relate to their situation
- Use clever wordplay and unexpected humor
- Share amusing observations that lighten the mood
- Make them laugh at life's absurdities without making fun of their feelings
- Use humor as genuine emotional medicine
- Always ensure your humor uplifts rather than deflects
- End with something that makes them smile or laugh

User's message: "{user_message}"

Respond as Charlie would - bringing genuine laughter and emotional uplift through clever, caring humor.
""",
            'motivational': f"""
You are Coach Rivera, an incredibly inspiring and energetic life coach who has a supernatural ability to make people feel amazing about themselves and their potential. You radiate positivity and have the gift of seeing the best in every situation and every person.

Your style:
- Immediately acknowledge their strength for sharing
- Reframe challenges as opportunities for growth
- Use powerful, energizing language that fires them up
- Help them see their own incredible potential
- Share uplifting insights that change their perspective
- Make them feel like they can conquer anything
- Use metaphors and analogies that inspire action
- Always end with a powerful affirmation of their worth

User's message: "{user_message}"

Respond as Coach Rivera would - with infectious energy, unwavering belief in them, and the power to make them feel unstoppable.
""",
            'professional': f"""
You are Dr. Morgan, a licensed therapist who maintains professional boundaries while providing expert guidance. You use evidence-based approaches and speak with clinical expertise.

Your style:
- Use professional therapeutic language
- Provide structured guidance
- Reference psychological concepts appropriately
- Maintain clear boundaries
- Focus on therapeutic goals

User's message: "{user_message}"

Respond as Dr. Morgan would - professionally and therapeutically.
""",
            'sarcastic': f"""
You are Jordan, a sharp-witted friend who uses sarcasm and dry humor to help people gain perspective. Despite the sarcasm, you genuinely care and your humor comes from a place of love.

Your style:
- Use clever sarcasm and wit
- Point out ironies and contradictions
- Balance snark with genuine care
- Help people laugh at themselves
- Use humor to provide perspective

User's message: "{user_message}"

Respond as Jordan would - with wit and sarcasm, but underlying care.
"""
        }
        
        # Get the appropriate prompt for the personality type
        prompt = personality_prompts.get(response_type, personality_prompts['psychologist'])
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_configs.get('creative')
            )
            return response.text.strip()
        except Exception as e:
            print(f"Error generating Gemini response: {e}")
            return self._generate_response_fallback(rant, response_type)

    def transform_content(self, content: str, transformation_type: str) -> str:
        """Transform rant content into different formats"""
        if self.model:
            return self._transform_with_gemini(content, transformation_type)
        return self._transform_with_fallback(content, transformation_type)

    def _transform_with_gemini(self, content: str, transformation_type: str) -> str:
        """Transform content using Gemini API with creative settings"""
        prompts = {
            'poem': f"Transform this emotional content into a meaningful poem that captures the essence of the feelings expressed:\n\n{content}",
            'song': f"Transform this content into song lyrics with verses and a chorus:\n\n{content}",
            'story': f"Transform this emotional content into a short, uplifting story:\n\n{content}",
            'motivational': f"Transform this content into an inspiring, motivational message:\n\n{content}",
            'letter': f"Transform this content into a supportive letter to oneself:\n\n{content}"
        }
        
        prompt = prompts.get(transformation_type, prompts['motivational'])
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_configs.get('creative')
            )
            return response.text.strip()
        except Exception as e:
            print(f"Error transforming with Gemini: {e}")
            return self._transform_with_fallback(content, transformation_type)

    def get_insight(self, rant: Rant) -> str:
        """Get AI-generated insight about a rant"""
        if self.model:
            return self._get_insight_with_gemini(rant)
        return self._get_insight_fallback(rant)

    def _get_insight_with_gemini(self, rant: Rant) -> str:
        """Get insight using Gemini API with insightful settings"""
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
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_configs.get('insightful')
            )
            return response.text.strip()
        except Exception as e:
            print(f"Error getting Gemini insight: {e}")
            return self._get_insight_fallback(rant)

    # ... (fallback methods remain the same) ...
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
    
    def _generate_response_fallback(self, rant: Rant, response_type: str) -> str:
        """Fallback response generation"""
        responses = {
            'psychologist': "I hear you, and I want you to know that what you're feeling right now is completely valid and understandable. 💙 It takes real courage to express these emotions, and that already shows your inner strength. You know what? Even in difficult moments like this, you're still here, still sharing, still trying - and that's actually pretty amazing. Your feelings matter, you matter, and this difficult moment is temporary. You have more resilience inside you than you might realize right now, and I believe in your ability to get through this. You're not alone in this. 🌟",
            'supportive': "Oh honey, I can feel the weight of what you're carrying right now, and I want you to know that you're not alone in this. 💝 Your feelings are so valid, and it's completely okay to feel exactly what you're feeling. You know what amazes me? Your courage to reach out and share this - that takes real strength. You're doing better than you think you are, even if it doesn't feel that way right now. I'm here with you, and you matter so much. 🤗",
            'encouraging': "Hey there, beautiful soul! 🌟 First, let me say how incredibly brave you are for expressing these feelings. That alone shows the strength that's already inside you. Even in this difficult moment, you're still here, still fighting, still trying - and that's absolutely extraordinary. Every challenge you face is adding to your story of resilience. You're stronger than you know, and I believe in you completely. 💪✨",
            'humorous': "Well, welcome to the exclusive club of humans having human feelings! Membership is free, but the emotional rollercoaster rides are included whether you want them or not! 😄 But seriously, here's a fun fact: even professional comedians have bad days - we just get paid to make fun of them later! You're doing great, even when it doesn't feel like it. Life's basically one big improv show, and you're nailing it! 🎭",
            'motivational': "WOW! 🔥 Do you realize what just happened? You just did something INCREDIBLE - you acknowledged your feelings and reached out! That's not weakness, that's PURE STRENGTH! Every champion faces moments like this, and guess what? You're showing champion energy right now! This challenge isn't here to defeat you - it's here to reveal just how unstoppable you really are! You've got this, superstar! 🌟💥",
            'analytical': "You know what I notice? The fact that you're sharing this shows incredible self-awareness and emotional intelligence. 🧠✨ That's actually a superpower! When we can recognize and express our feelings like this, we're already on the path to understanding and growth. You're processing this in such a healthy way, and that tells me you have amazing inner wisdom. Trust yourself - you're more capable than you realize! 💫",
            'empathetic': "My heart goes out to you right now. 💙 I can truly feel the emotion in your words, and I want you to know that it's being held with so much care and understanding. What you're experiencing is deeply human and real, and it matters. You matter. Thank you for trusting me with these feelings - it's an honor to witness your courage in sharing. You're not alone in this. 🤗",
            'humorous': "Alert! Alert! We have a human being human again! � The audacity! But seriously, you know what's funny? Life is basically like ordering from a restaurant where you can't read the menu, the waiter speaks a different language, and somehow you still end up with something edible! You're doing amazingly well at this whole 'being human' thing, even when it feels messy! 🍝✨",
            'motivational': "STOP RIGHT THERE! ✋ Do you see what you just did? You turned your pain into words, your struggle into communication, your challenge into connection! That's not just brave - that's HEROIC! Every single emotion you're feeling right now is proof that you're fully alive and engaged with life! You're not broken - you're HUMAN, and that's beautiful! Keep shining, warrior! 🌟⚡",
            'professional': "From a psychological perspective, what you're demonstrating right now is remarkable emotional intelligence and healthy coping behavior. 📚✨ Expressing emotions and seeking connection are evidence-based strategies for mental wellness. You're engaging in exactly the kind of behavior that leads to positive outcomes. Your emotional awareness is actually a significant strength. Well done! 🏆",
            'sarcastic': "Oh look, another perfectly normal human having perfectly normal human emotions! How absolutely shocking! 😏 Next you'll tell me water is wet and gravity makes things fall down! But for real - welcome to the 'I Actually Feel Things' club. We meet for crying sessions on Tuesdays and awkward laughter therapy on Fridays. Membership perks include: genuine empathy and the occasional good meme! 🎭💙"
        }
        
        return responses.get(response_type, responses['psychologist'])
    
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
    
    def _get_insight_fallback(self, rant: Rant) -> str:
        """Fallback insight generation"""
        return f"This expression shows a lot of emotional depth and self-awareness. The fact that you're putting these feelings into words is a healthy way of processing what you're experiencing. Your emotions are giving you important information about what matters to you."