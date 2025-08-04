import requests
import json
from typing import Dict, Any
from flask import current_app
from app.models import Rant, EmotionType
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: Google Generative AI not available")

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: OpenAI not available")

class AIService:
    """Main AI service for processing rants and generating insights"""
    
    def __init__(self, app=None):
        self.app = app
        self.openai_key = None
        self.gemini_key = None
        self.gemini_model = None
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with Flask app"""
        self.app = app
        with app.app_context():
            self.openai_key = app.config.get('OPENAI_API_KEY')
            self.gemini_key = app.config.get('GEMINI_API_KEY')
            
            # Initialize Gemini first (priority)
            if GEMINI_AVAILABLE and self.gemini_key:
                try:
                    genai.configure(api_key=self.gemini_key)
                    self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model name
                    print("✅ Gemini AI initialized successfully!")
                except Exception as e:
                    print(f"❌ Error initializing Gemini: {e}")
                    self.gemini_model = None
            
            # Initialize OpenAI as fallback
            if OPENAI_AVAILABLE and self.openai_key:
                try:
                    import openai
                    openai.api_key = self.openai_key
                    print("✅ OpenAI initialized as fallback")
                except Exception as e:
                    print(f"❌ Error initializing OpenAI: {e}")
    
    def analyze_rant(self, rant: Rant) -> Dict[str, Any]:
        """Analyze a rant for emotion, sentiment, and keywords using Gemini AI"""
        if not self.gemini_model:
            raise Exception("Gemini AI is required for rant analysis but is not available")
        
        try:
            print("🤖 Using Gemini AI for rant analysis")
            return self._analyze_with_gemini(rant)
        except Exception as e:
            print(f"Error analyzing rant with Gemini: {e}")
            # Re-raise the error to ensure we don't fall back to local methods
            raise Exception(f"Gemini AI analysis failed: {e}")
    
    def _analyze_with_openai(self, rant: Rant) -> Dict[str, Any]:
        """Analyze rant using OpenAI API"""
        prompt = f"""
        Analyze the following rant and provide:
        1. Primary emotion (angry, frustrated, sad, anxious, excited, happy, confused, neutral)
        2. Emotion confidence (0-1)
        3. Sentiment score (-1 to 1)
        4. Key keywords/topics (max 10)
        5. Brief summary of the main issue
        
        Rant: "{rant.content}"
        
        Respond in JSON format:
        {{
            "emotion": "emotion_name",
            "emotion_confidence": 0.0,
            "sentiment_score": 0.0,
            "keywords": ["keyword1", "keyword2"],
            "summary": "brief summary",
            "main_issue": "main concern"
        }}
        """
        
        try:
            import openai
            # Set the API key
            openai.api_key = self.openai_key
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert emotion and sentiment analyzer. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            # Extract content from response safely
            content = None
            try:
                # Try the most common attribute access pattern
                content = getattr(getattr(getattr(response, 'choices', [None])[0], 'message', None), 'content', None)
            except (AttributeError, IndexError, TypeError):
                pass
            
            if not content:
                try:
                    # Try alternative attribute access
                    content = getattr(getattr(response, 'choices', [None])[0], 'text', None)
                except (AttributeError, IndexError, TypeError):
                    pass
            
            if not content:
                try:
                    # Convert response to string and parse if needed
                    response_str = str(response)
                    if 'choices' in response_str:
                        # Try to extract content using string manipulation as last resort
                        import re
                        content_match = re.search(r'"content":\s*"([^"]*)"', response_str)
                        if content_match:
                            content = content_match.group(1)
                except Exception:
                    pass
            
            if not content:
                raise ValueError("Could not extract content from OpenAI response")
            
            result = json.loads(content)
            
            # Convert emotion string to enum
            emotion_str = result.get('emotion', 'neutral').lower()
            emotion_mapping = {
                'angry': EmotionType.ANGRY,
                'frustrated': EmotionType.FRUSTRATED,
                'sad': EmotionType.SAD,
                'anxious': EmotionType.ANXIOUS,
                'excited': EmotionType.EXCITED,
                'happy': EmotionType.HAPPY,
                'confused': EmotionType.CONFUSED,
                'neutral': EmotionType.NEUTRAL
            }
            
            result['emotion'] = emotion_mapping.get(emotion_str, EmotionType.NEUTRAL)
            result['keywords'] = json.dumps(result.get('keywords', []))
            
            return result
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._get_fallback_analysis(rant)
    
    def _analyze_with_gemini(self, rant: Rant) -> Dict[str, Any]:
        """Analyze rant using Gemini API - no fallbacks"""
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
            response = self.gemini_model.generate_content(prompt)
            
            if not response.text:
                raise Exception("Gemini returned empty response for analysis")
            
            # Clean the response to extract only the JSON part
            cleaned_response = response.text.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            
            result = json.loads(cleaned_response)

            # Convert emotion string to enum
            emotion_str = result.get('emotion', 'neutral').lower()
            emotion_mapping = {
                'angry': EmotionType.ANGRY,
                'frustrated': EmotionType.FRUSTRATED,
                'sad': EmotionType.SAD,
                'anxious': EmotionType.ANXIOUS,
                'excited': EmotionType.EXCITED,
                'happy': EmotionType.HAPPY,
                'confused': EmotionType.CONFUSED,
                'neutral': EmotionType.NEUTRAL
            }
            
            result['emotion'] = emotion_mapping.get(emotion_str, EmotionType.NEUTRAL)
            result['keywords'] = json.dumps(result.get('keywords', []))
            
            return result
            
        except Exception as e:
            raise Exception(f"Gemini analysis failed: {e}")

    def _analyze_with_local_model(self, rant: Rant) -> Dict[str, Any]:
        """Analyze rant using local/simple model"""
        content = rant.content.lower()
        
        # Emotion detection based on keywords
        emotion_keywords = {
            EmotionType.ANGRY: ['angry', 'furious', 'rage', 'mad', 'pissed', 'hate'],
            EmotionType.FRUSTRATED: ['frustrated', 'annoyed', 'irritated', 'upset'],
            EmotionType.SAD: ['sad', 'depressed', 'down', 'cry', 'tears', 'heartbroken'],
            EmotionType.ANXIOUS: ['anxious', 'worried', 'nervous', 'stress', 'panic'],
            EmotionType.EXCITED: ['excited', 'thrilled', 'amazing', 'awesome', 'incredible'],
            EmotionType.HAPPY: ['happy', 'joy', 'great', 'wonderful', 'fantastic'],
            EmotionType.CONFUSED: ['confused', 'lost', 'unsure', 'don\'t know', 'unclear']
        }
        
        emotion_scores = {}
        for emotion, keywords in emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in content)
            emotion_scores[emotion] = score
        
        # Find dominant emotion
        if emotion_scores and any(emotion_scores.values()):
            dominant_emotion = max(emotion_scores, key=lambda k: emotion_scores[k])
            max_score = emotion_scores[dominant_emotion]
        else:
            dominant_emotion = EmotionType.NEUTRAL
            max_score = 0
        if max_score == 0:
            dominant_emotion = EmotionType.NEUTRAL
            confidence = 0.5
        else:
            total_words = len(content.split())
            confidence = min(max_score / total_words * 10, 1.0)
        
        # Simple sentiment analysis
        positive_words = ['good', 'great', 'amazing', 'awesome', 'love', 'happy', 'fantastic']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'horrible', 'worst', 'sucks']
        
        positive_count = sum(1 for word in positive_words if word in content)
        negative_count = sum(1 for word in negative_words if word in content)
        
        if positive_count + negative_count == 0:
            sentiment_score = 0.0
        else:
            sentiment_score = (positive_count - negative_count) / (positive_count + negative_count)
        
        # Extract keywords (simple approach)
        words = content.split()
        keywords = [word for word in words if len(word) > 4][:10]
        
        return {
            'emotion': dominant_emotion.value,
            'emotion_confidence': confidence,
            'sentiment_score': sentiment_score,
            'keywords': json.dumps(keywords),
            'summary': content[:100] + '...' if len(content) > 100 else content,
            'main_issue': 'General concern'
        }

    def _get_fallback_analysis(self, rant: Rant) -> Dict[str, Any]:
        """Fallback analysis when other methods fail"""
        return {
            'emotion': EmotionType.NEUTRAL,
            'emotion_confidence': 0.5,
            'sentiment_score': 0.0,
            'keywords': json.dumps(['general', 'rant']),
            'summary': rant.content[:100] + '...' if len(rant.content) > 100 else rant.content,
            'main_issue': 'Unable to analyze'
        }
    
    def suggest_actions(self, rant: Rant) -> list:
        """Generate action suggestions based on rant analysis"""
        actions = []
        
        if not rant.detected_emotion:
            return actions
        
        emotion = rant.detected_emotion
        
        if emotion == EmotionType.ANGRY:
            actions = [
                {
                    'type': 'exercise',
                    'title': 'Physical Exercise',
                    'description': 'Go for a run or hit the gym to release anger',
                    'priority': 5
                },
                {
                    'type': 'meditate',
                    'title': 'Breathing Exercise',
                    'description': 'Try deep breathing or meditation to calm down',
                    'priority': 4
                },
                {
                    'type': 'call_friend',
                    'title': 'Talk to Someone',
                    'description': 'Call a trusted friend or family member',
                    'priority': 3
                }
            ]
        
        elif emotion == EmotionType.SAD:
            actions = [
                {
                    'type': 'call_friend',
                    'title': 'Reach Out',
                    'description': 'Connect with someone who cares about you',
                    'priority': 5
                },
                {
                    'type': 'book_therapy',
                    'title': 'Professional Help',
                    'description': 'Consider talking to a therapist or counselor',
                    'priority': 4
                },
                {
                    'type': 'exercise',
                    'title': 'Light Exercise',
                    'description': 'Try a gentle walk or yoga session',
                    'priority': 3
                }
            ]
        
        elif emotion == EmotionType.ANXIOUS:
            actions = [
                {
                    'type': 'meditate',
                    'title': 'Mindfulness Practice',
                    'description': 'Try guided meditation or mindfulness exercises',
                    'priority': 5
                },
                {
                    'type': 'create_reminder',
                    'title': 'Action Plan',
                    'description': 'Break down your worries into actionable steps',
                    'priority': 4
                },
                {
                    'type': 'call_friend',
                    'title': 'Get Support',
                    'description': 'Talk through your concerns with someone',
                    'priority': 3
                }
            ]
        
        elif emotion == EmotionType.EXCITED:
            actions = [
                {
                    'type': 'share_social',
                    'title': 'Share Your Joy',
                    'description': 'Share your excitement on social media',
                    'priority': 4
                },
                {
                    'type': 'create_reminder',
                    'title': 'Plan Something',
                    'description': 'Channel your energy into planning something fun',
                    'priority': 3
                }
            ]
        
        else:  # Default actions
            actions = [
                {
                    'type': 'save_local',
                    'title': 'Save This Moment',
                    'description': 'Keep a record of your thoughts',
                    'priority': 2
                },
                {
                    'type': 'share_social',
                    'title': 'Share If You Want',
                    'description': 'Consider sharing your thoughts with others',
                    'priority': 1
                }
            ]
        
        return actions
    
    def get_ai_response(self, rant: Rant, personality: str = 'supportive') -> str:
        """Generate AI response based on personality using Gemini AI"""
        if not self.gemini_model:
            raise Exception("Gemini AI is required for response generation but is not available")
        
        try:
            return self._generate_response_with_gemini(rant, personality)
        except Exception as e:
            print(f"Error generating response with Gemini: {e}")
            # Re-raise the error to ensure we don't fall back to local methods
            raise Exception(f"Gemini AI response generation failed: {e}")
    
    def _generate_response_with_openai(self, rant: Rant, personality: str) -> str:
        """Generate response using OpenAI"""
        personality_prompts = {
            'supportive': "You are a supportive, empathetic friend who listens and offers comfort.",
            'sarcastic': "You are witty and sarcastic, but ultimately caring and helpful.",
            'humorous': "You use humor to lighten the mood while being understanding.",
            'motivational': "You are an energetic motivational coach who inspires action.",
            'professional': "You are a professional counselor providing thoughtful guidance."
        }
        
        system_prompt = personality_prompts.get(personality, personality_prompts['supportive'])
        
        try:
            import openai
            openai.api_key = self.openai_key
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Someone just shared this with me: '{rant.content}'. How should I respond?"}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            # Extract content safely
            content = None
            try:
                content = getattr(getattr(getattr(response, 'choices', [None])[0], 'message', None), 'content', None)
            except (AttributeError, IndexError, TypeError):
                pass
            
            if not content:
                try:
                    content = getattr(getattr(response, 'choices', [None])[0], 'text', None)
                except (AttributeError, IndexError, TypeError):
                    pass
            
            if content:
                return content.strip()
            else:
                return self._generate_response_local(rant, personality)
                
        except Exception as e:
            print(f"OpenAI response error: {e}")
            return self._generate_response_local(rant, personality)
    
    def _generate_response_local(self, rant: Rant, personality: str) -> str:
        """Generate response using local templates"""
        responses = {
            'supportive': [
                "I hear you, and what you're feeling is completely valid.",
                "That sounds really tough. You're not alone in this.",
                "Thank you for sharing that with me. It takes courage to express how you feel."
            ],
            'sarcastic': [
                "Well, that's one way to look at it... but seriously, I get it.",
                "Life's really testing you, huh? But you've got this.",
                "Oh, the universe is just full of surprises, isn't it? But for real, that's rough."
            ],
            'humorous': [
                "Life's like a comedy show, except sometimes the jokes are on us!",
                "Well, at least you're not alone in the 'life is weird' club!",
                "That's definitely going in the 'things that make you go hmm' category!"
            ],
            'motivational': [
                "This is just a chapter, not your whole story! You've got the power to change things!",
                "Every challenge is an opportunity to grow stronger. You're already on your way!",
                "I believe in you! This too shall pass, and you'll come out stronger!"
            ],
            'professional': [
                "It sounds like you're dealing with a challenging situation. Let's explore some ways to address this.",
                "Your feelings are valid, and it's important to acknowledge them. What would feel most helpful right now?",
                "Thank you for sharing. It's clear this is important to you. How can we work through this together?"
            ]
        }
        
        import random
        return random.choice(responses.get(personality, responses['supportive']))
    
    def _get_fallback_response(self, rant: Rant, personality: str) -> str:
        """Fallback response when other methods fail"""
        return "I hear you, and I'm here to listen. Sometimes just expressing how we feel can be helpful."

    def transform_to_poem(self, content: str) -> str:
        """Transform content into a poem using Gemini AI"""
        if not self.gemini_model:
            raise Exception("Gemini AI is required for poem transformation but is not available")
        return self._transform_to_poem_with_gemini(content)
    
    def transform_to_song(self, content: str) -> str:
        """Transform content into song lyrics using Gemini AI"""
        if not self.gemini_model:
            raise Exception("Gemini AI is required for song transformation but is not available")
        return self._transform_to_song_with_gemini(content)
    
    def transform_to_story(self, content: str) -> str:
        """Transform content into a short story using Gemini AI"""
        if not self.gemini_model:
            raise Exception("Gemini AI is required for story transformation but is not available")
        return self._transform_to_story_with_gemini(content)
    
    def transform_to_motivational(self, content: str) -> str:
        """Transform content into motivational message using Gemini AI"""
        if not self.gemini_model:
            raise Exception("Gemini AI is required for motivational transformation but is not available")
        return self._transform_to_motivational_with_gemini(content)
    
    def _transform_to_poem_with_gemini(self, content):
        """Transform content to poem using Gemini - no fallbacks"""
        prompt = f"""Transform the following text into a beautiful, creative poem. Make it emotional and artistic:

{content}

Create a poem with proper structure, rhythm, and emotional depth."""
        
        try:
            response = self.gemini_model.generate_content(prompt)
            if response.text:
                return response.text
            else:
                raise Exception("Gemini returned empty response for poem generation")
        except Exception as e:
            raise Exception(f"Gemini poem generation failed: {e}")

    def _transform_to_song_with_gemini(self, content):
        """Transform content to song using Gemini - no fallbacks"""
        prompt = f"""Transform the following text into song lyrics with verses, chorus, and bridge. Make it emotional and musical:

{content}

Create structured song lyrics with:
- Verse 1
- Chorus
- Verse 2
- Chorus
- Bridge
- Final Chorus"""
        
        try:
            response = self.gemini_model.generate_content(prompt)
            if response.text:
                return response.text
            else:
                raise Exception("Gemini returned empty response for song generation")
        except Exception as e:
            raise Exception(f"Gemini song generation failed: {e}")

    def _transform_to_story_with_gemini(self, content):
        """Transform content to story using Gemini - no fallbacks"""
        prompt = f"""Transform the following text into an engaging short story. Make it narrative and compelling:

{content}

Create a complete short story with:
- Setting and characters
- Conflict and resolution
- Emotional depth
- Satisfying conclusion"""
        
        try:
            response = self.gemini_model.generate_content(prompt)
            if response.text:
                return response.text
            else:
                raise Exception("Gemini returned empty response for story generation")
        except Exception as e:
            raise Exception(f"Gemini story generation failed: {e}")

    def _transform_to_motivational_with_gemini(self, content):
        """Transform content to motivational message using Gemini - no fallbacks"""
        prompt = f"""Transform the following text into a powerful, uplifting motivational message. Make it inspiring and actionable:

{content}

Create a motivational message that:
- Acknowledges the challenge
- Provides perspective
- Offers actionable advice
- Inspires hope and determination"""
        
        try:
            response = self.gemini_model.generate_content(prompt)
            if response.text:
                return response.text
            else:
                raise Exception("Gemini returned empty response for motivational generation")
        except Exception as e:
            raise Exception(f"Gemini motivational generation failed: {e}")
        except Exception as e:
            print(f"Gemini motivational message generation error: {e}")
            return self._transform_to_motivational_local(content)

    def _transform_to_motivational_with_openai(self, content):
        # Stubbed for production safety
        return self._transform_to_motivational_local(content)

    def _generate_response_with_gemini(self, rant: Rant, personality: str) -> str:
        """Generate response using Gemini - no fallbacks"""
        personality_prompts = {
            'supportive': "You are a supportive, empathetic friend who listens and offers comfort.",
            'sarcastic': "You are witty and sarcastic, but ultimately caring and helpful.",
            'humorous': "You use humor to lighten the mood while being understanding.",
            'motivational': "You are an energetic motivational coach who inspires action.",
            'professional': "You are a professional counselor providing thoughtful guidance."
        }
        
        system_prompt = personality_prompts.get(personality, personality_prompts['supportive'])
        
        prompt = f"""{system_prompt}

Someone just shared this with me: '{rant.content}'. 

Please provide a thoughtful, caring response that matches my personality. Be genuine, empathetic, and helpful."""

        try:
            response = self.gemini_model.generate_content(prompt)
            if response.text:
                return response.text
            else:
                raise Exception("Gemini returned empty response")
        except Exception as e:
            raise Exception(f"Gemini response generation failed: {e}")

    # Fallback/local transformation and response methods
    def _transform_to_song_local(self, content):
        lines = content.split('.')
        verse1 = []
        chorus = []
        for i, line in enumerate(lines[:6]):
            if line.strip():
                if i < 3:
                    verse1.append(line.strip())
                else:
                    chorus.append(line.strip())
        song = "[Verse 1]\n"
        song += "\n".join(verse1)
        song += "\n\n[Chorus]\n"
        song += "\n".join(chorus)
        return song

    def _transform_to_story_local(self, content):
        return f"Once upon a time, there was someone who felt exactly like this: {content}\n\nThey discovered that their feelings were valid, and through understanding themselves better, they found a way forward."

    def _transform_to_motivational_local(self, content):
        return f"I hear you, and your feelings are completely valid. {content}\n\nRemember: Every challenge is an opportunity to grow stronger. You have the power to overcome this, and you're not alone in this journey. Take it one step at a time."

    def _generate_response_fallback(self, rant, response_type):
        responses = {
            'supportive': "I hear you, and your feelings are completely valid. It sounds like you're going through a challenging time, and that's okay. Remember that it's normal to feel this way, and you're not alone in experiencing these emotions.",
            'encouraging': "Your feelings matter, and it's brave of you to express them. Every challenge you face is helping you grow stronger, even when it's doesn't feel that way. You have the strength to get through this.",
            'analytical': "It seems like this situation is really affecting you. Sometimes it helps to break down what's happening and look at it from different angles. What do you think might be the root cause of these feelings?",
            'empathetic': "I can really feel the emotion in your words. It must be difficult to be experiencing this right now. Know that your feelings are heard and understood."
        }
        return responses.get(response_type, responses['supportive'])

    def _transform_to_poem_local(self, content):
        return f"In words unspoken, feelings deep,\n{content[:50]}...\nThrough darkness comes the light we seek,\nAnd peace at last, our hearts can keep."
