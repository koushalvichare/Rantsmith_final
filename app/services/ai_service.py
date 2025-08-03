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
                    self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                    print("✅ Gemini AI initialized successfully!")
                except Exception as e:
                    print(f"❌ Error initializing Gemini: {e}")
                    self.gemini_model = None
            
            # Initialize OpenAI as fallback
            if OPENAI_AVAILABLE and self.openai_key:
                try:
                    openai.api_key = self.openai_key
                    print("✅ OpenAI initialized as fallback")
                except Exception as e:
                    print(f"❌ Error initializing OpenAI: {e}")
    
    def analyze_rant(self, rant: Rant) -> Dict[str, Any]:
        """Analyze a rant for emotion, sentiment, and keywords"""
        try:
            # Prioritize Gemini AI over OpenAI
            if self.gemini_model and self.gemini_key:
                print("🤖 Using Gemini AI for rant analysis")
                return self._analyze_with_gemini(rant)
            elif OPENAI_AVAILABLE and self.openai_key:
                print("🤖 Using OpenAI for rant analysis")
                return self._analyze_with_openai(rant)
            else:
                print("🤖 Using local model for rant analysis")
                return self._analyze_with_local_model(rant)
        except Exception as e:
            print(f"Error analyzing rant: {e}")
            return self._get_fallback_analysis(rant)
    
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
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert emotion and sentiment analyzer. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            
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
            response = self.gemini_model.generate_content(prompt)
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
            return self._get_fallback_analysis(rant)

    def _analyze_with_local_model(self, rant: Rant) -> Dict[str, Any]:
        """Analyze rant using local/simple model"""
        # Simple keyword-based analysis
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
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        max_score = emotion_scores[dominant_emotion]
        
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
            'emotion': dominant_emotion.value,  # Convert enum to string
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
        """Generate AI response based on personality"""
        try:
            if self.openai_key:
                return self._generate_response_with_openai(rant, personality)
            else:
                return self._generate_response_local(rant, personality)
        except Exception as e:
            print(f"Error generating response: {e}")
            return self._get_fallback_response(rant, personality)
    
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
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Someone just shared this with me: '{rant.content}'. How should I respond?"}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
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
        """Transform content into a poem"""
        try:
            if self.gemini_model and self.gemini_key:
                return self._transform_to_poem_with_gemini(content)
            elif self.openai_key:
                return self._transform_to_poem_with_openai(content)
            else:
                return self._transform_to_poem_local(content)
        except Exception as e:
            print(f"Error transforming to poem: {e}")
            return self._fallback_poem_transform(content)
    
    def transform_to_song(self, content: str) -> str:
        """Transform content into song lyrics"""
        try:
            if self.gemini_model and self.gemini_key:
                return self._transform_to_song_with_gemini(content)
            elif self.openai_key:
                return self._transform_to_song_with_openai(content)
            else:
                return self._transform_to_song_local(content)
        except Exception as e:
            print(f"Error transforming to song: {e}")
            return self._fallback_song_transform(content)
    
    def transform_to_story(self, content: str) -> str:
        """Transform content into a short story"""
        try:
            if self.gemini_model and self.gemini_key:
                return self._transform_to_story_with_gemini(content)
            elif self.openai_key:
                return self._transform_to_story_with_openai(content)
            else:
                return self._transform_to_story_local(content)
        except Exception as e:
            print(f"Error transforming to story: {e}")
            return self._fallback_story_transform(content)
    
    def transform_to_motivational(self, content: str) -> str:
        """Transform content into motivational message"""
        try:
            if self.gemini_model and self.gemini_key:
                return self._transform_to_motivational_with_gemini(content)
            elif self.openai_key:
                return self._transform_to_motivational_with_openai(content)
            else:
                return self._transform_to_motivational_local(content)
        except Exception as e:
            print(f"Error transforming to motivational: {e}")
            return self._fallback_motivational_transform(content)
    
    def _transform_to_poem_with_gemini(self, content: str) -> str:
        """Transform content to poem using Gemini"""
        prompt = f"""
        Transform the following emotional content into a beautiful, meaningful poem. 
        Keep the core emotion and meaning, but express it poetically:
        
        "{content}"
        
        Please create a poem that:
        - Captures the essence of the feelings expressed
        - Uses poetic language and imagery
        - Has a meaningful structure
        - Provides comfort or insight
        
        Return only the poem, no additional text.
        """
        
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error with Gemini poem transformation: {e}")
            return self._transform_to_poem_local(content)

    def _transform_to_poem_with_openai(self, content: str) -> str:
        """Transform content to poem using OpenAI"""
        prompt = f"""
        Transform the following text into a beautiful poem. Keep the core emotion and meaning, but express it poetically:
        
        "{content}"
        
        Return only the poem, no additional text.
        """
        
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            temperature=0.8
        )
        
        return response.choices[0].text.strip()

    def _transform_to_song_with_gemini(self, content: str) -> str:
        """Transform content to song using Gemini"""
        prompt = f"""
        Transform the following emotional content into song lyrics with verses and a chorus. 
        Keep the emotion and meaning:
        
        "{content}"
        
        Please create song lyrics that:
        - Have a clear verse-chorus structure
        - Capture the emotional essence
        - Are meaningful and relatable
        - Flow well musically
        
        Return only the song lyrics, no additional text.
        """
        
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error with Gemini song transformation: {e}")
            return self._transform_to_song_local(content)

    def _transform_to_story_with_gemini(self, content: str) -> str:
        """Transform content to story using Gemini"""
        prompt = f"""
        Transform the following emotional content into a short, uplifting story. 
        Make it relatable and inspiring:
        
        "{content}"
        
        Please create a story that:
        - Reflects the emotions expressed
        - Has a positive or hopeful resolution
        - Is relatable to the reader
        - Provides comfort or insight
        
        Return only the story, no additional text.
        """
        
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error with Gemini story transformation: {e}")
            return self._transform_to_story_local(content)

    def _transform_to_motivational_with_gemini(self, content: str) -> str:
        """Transform content to motivational message using Gemini"""
        prompt = f"""
        Transform the following emotional content into an inspiring, motivational message. 
        Provide encouragement and perspective:
        
        "{content}"
        
        Please create a motivational message that:
        - Acknowledges the person's feelings
        - Provides encouragement and hope
        - Offers practical perspective
        - Is uplifting and supportive
        
        Return only the motivational message, no additional text.
        """
        
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error with Gemini motivational transformation: {e}")
            return self._transform_to_motivational_local(content)

    def _transform_to_song_with_openai(self, content: str) -> str:
        """Transform content to song using OpenAI"""
        prompt = f"""
        Transform the following text into song lyrics with verses and a chorus. Keep the emotion and meaning:
        
        "{content}"
        
        Format as:
        [Verse 1]
        ...
        [Chorus]
        ...
        [Verse 2]
        ...
        [Chorus]
        ...
        """
        
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=300,
            temperature=0.8
        )
        
        return response.choices[0].text.strip()

    def _transform_to_song_local(self, content: str) -> str:
        """Local fallback for song transformation"""
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
    
    def _transform_to_story_local(self, content: str) -> str:
        """Local fallback for story transformation"""
        return f"Once upon a time, there was someone who felt exactly like this: {content}\n\nThey discovered that their feelings were valid, and through understanding themselves better, they found a way forward."
    
    def _transform_to_motivational_local(self, content: str) -> str:
        """Local fallback for motivational transformation"""
        return f"I hear you, and your feelings are completely valid. {content}\n\nRemember: Every challenge is an opportunity to grow stronger. You have the power to overcome this, and you're not alone in this journey. Take it one step at a time."
    
    def _fallback_poem_transform(self, content: str) -> str:
        """Fallback poem transformation"""
        return f"In words unspoken, feelings deep,\n{content[:50]}...\nThrough darkness comes the light we seek,\nAnd peace at last, our hearts can keep."
    
    def _fallback_song_transform(self, content: str) -> str:
        """Fallback song transformation"""
        return f"[Verse 1]\n{content[:100]}...\n\n[Chorus]\nEvery feeling has its place\nEvery struggle shows your strength\nIn this moment, find your grace\nYou will go to any length"
    
    def _fallback_story_transform(self, content: str) -> str:
        """Fallback story transformation"""
        return f"There once was a person who felt deeply about their situation. {content[:150]}... And in that moment of vulnerability, they realized that their feelings were the first step toward positive change."
    
    def _fallback_motivational_transform(self, content: str) -> str:
        """Fallback motivational transformation"""
        return f"Your feelings matter, and this experience is shaping you into someone stronger. {content[:100]}... Remember: You are capable of amazing things, and this too shall pass."

    def generate_response(self, rant: Rant, response_type: str = "supportive") -> str:
        """Generate a supportive response to a rant"""
        try:
            if self.gemini_model and self.gemini_key:
                return self._generate_response_with_gemini(rant, response_type)
            elif self.openai_key:
                return self._generate_response_with_openai(rant, response_type)
            else:
                return self._generate_response_fallback(rant, response_type)
        except Exception as e:
            print(f"Error generating response: {e}")
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
            response = self.gemini_model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating Gemini response: {e}")
            return self._generate_response_fallback(rant, response_type)
    
    def _generate_response_with_openai(self, rant: Rant, response_type: str) -> str:
        """Generate response using OpenAI API"""
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
        
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            temperature=0.7
        )
        
        return response.choices[0].text.strip()
    
    def _generate_response_fallback(self, rant: Rant, response_type: str) -> str:
        """Fallback response generation"""
        responses = {
            'supportive': "I hear you, and your feelings are completely valid. It sounds like you're going through a challenging time, and that's okay. Remember that it's normal to feel this way, and you're not alone in experiencing these emotions.",
            'encouraging': "Your feelings matter, and it's brave of you to express them. Every challenge you face is helping you grow stronger, even when it doesn't feel that way. You have the strength to get through this.",
            'analytical': "It seems like this situation is really affecting you. Sometimes it helps to break down what's happening and look at it from different angles. What do you think might be the root cause of these feelings?",
            'empathetic': "I can really feel the emotion in your words. It must be difficult to be experiencing this right now. Know that your feelings are heard and understood."
        }
        
        return responses.get(response_type, responses['supportive'])
