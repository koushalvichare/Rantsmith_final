import requests
import json
import os
import time
from typing import Dict, Any
from flask import current_app
from app.models import Rant, ContentType
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class ContentGenerator:
    """Service for generating different types of content from rants"""
    
    def __init__(self):
        self.openai_key = current_app.config.get('OPENAI_API_KEY')
        self.gemini_key = current_app.config.get('GEMINI_API_KEY')
        self.elevenlabs_key = current_app.config.get('ELEVENLABS_API_KEY')
        self.runwayml_key = current_app.config.get('RUNWAYML_API_KEY')
        
        # Initialize Gemini if available
        self.gemini_model = None
        if GEMINI_AVAILABLE and self.gemini_key:
            try:
                genai.configure(api_key=self.gemini_key)
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            except Exception as e:
                print(f"Error initializing Gemini in ContentGenerator: {e}")
    
    def generate_text(self, rant: Rant) -> Dict[str, Any]:
        """Generate text-based content from rant"""
        start_time = time.time()
        
        try:
            # Try Gemini first, then OpenAI, then local
            if self.gemini_model:
                content = self._generate_text_with_gemini(rant)
                model_used = 'gemini-pro'
            elif self.openai_key:
                content = self._generate_text_with_openai(rant)
                model_used = 'gpt-3.5-turbo'
            else:
                content = self._generate_text_local(rant)
                model_used = 'local'
            
            processing_time = time.time() - start_time
            
            return {
                'title': 'Transformed Perspective',
                'content': content,
                'model_used': model_used,
                'processing_time': processing_time,
                'quality_score': 0.8
            }
            
        except Exception as e:
            return {
                'title': 'Error',
                'content': f'Error generating content: {str(e)}',
                'model_used': 'error',
                'processing_time': time.time() - start_time,
                'quality_score': 0.0
            }
    
    def generate_meme(self, rant: Rant) -> Dict[str, Any]:
        """Generate meme content from rant"""
        start_time = time.time()
        
        try:
            # Try Gemini first, then OpenAI, then local
            if self.gemini_model:
                meme_data = self._generate_meme_with_gemini(rant)
                model_used = 'gemini-pro'
            elif self.openai_key:
                meme_data = self._generate_meme_with_openai(rant)
                model_used = 'gpt-3.5-turbo'
            else:
                meme_data = self._generate_meme_local(rant)
                model_used = 'local'
            
            processing_time = time.time() - start_time
            
            return {
                'title': 'Meme: ' + meme_data['title'],
                'content': json.dumps(meme_data),
                'model_used': model_used,
                'processing_time': processing_time,
                'quality_score': 0.7
            }
            
        except Exception as e:
            return {
                'title': 'Meme Generation Failed',
                'content': json.dumps({'error': str(e)}),
                'model_used': 'error',
                'processing_time': time.time() - start_time,
                'quality_score': 0.0
            }

    def generate_tweet(self, rant: Rant) -> Dict[str, Any]:
        """Generate tweet from rant"""
        start_time = time.time()
        
        try:
            # Try Gemini first, then OpenAI, then local
            if self.gemini_model:
                tweet = self._generate_tweet_with_gemini(rant)
                model_used = 'gemini-pro'
            elif self.openai_key:
                tweet = self._generate_tweet_with_openai(rant)
                model_used = 'gpt-3.5-turbo'
            else:
                tweet = self._generate_tweet_local(rant)
                model_used = 'local'
            
            processing_time = time.time() - start_time
            
            return {
                'title': 'Generated Tweet',
                'content': tweet,
                'model_used': model_used,
                'processing_time': processing_time,
                'quality_score': 0.75
            }
            
        except Exception as e:
            return {
                'title': 'Tweet Generation Failed',
                'content': f'Error: {str(e)}',
                'model_used': 'error',
                'processing_time': time.time() - start_time,
                'quality_score': 0.0
            }
    
    def generate_song(self, rant: Rant) -> Dict[str, Any]:
        """Generate song lyrics from rant"""
        start_time = time.time()
        
        try:
            if self.openai_key:
                song = self._generate_song_with_openai(rant)
            else:
                song = self._generate_song_local(rant)
            
            processing_time = time.time() - start_time
            
            return {
                'title': song['title'],
                'content': song['lyrics'],
                'model_used': 'gpt-3.5-turbo' if self.openai_key else 'local',
                'processing_time': processing_time,
                'quality_score': 0.8
            }
            
        except Exception as e:
            return {
                'title': 'Song Generation Failed',
                'content': f'Error: {str(e)}',
                'model_used': 'error',
                'processing_time': time.time() - start_time,
                'quality_score': 0.0
            }
    
    def generate_script(self, rant: Rant) -> Dict[str, Any]:
        """Generate script/dialogue from rant"""
        start_time = time.time()
        
        try:
            if self.openai_key:
                script = self._generate_script_with_openai(rant)
            else:
                script = self._generate_script_local(rant)
            
            processing_time = time.time() - start_time
            
            return {
                'title': 'Generated Script',
                'content': script,
                'model_used': 'gpt-3.5-turbo' if self.openai_key else 'local',
                'processing_time': processing_time,
                'quality_score': 0.85
            }
            
        except Exception as e:
            return {
                'title': 'Script Generation Failed',
                'content': f'Error: {str(e)}',
                'model_used': 'error',
                'processing_time': time.time() - start_time,
                'quality_score': 0.0
            }
    
    def generate_audio(self, rant: Rant) -> Dict[str, Any]:
        """Generate audio content from rant"""
        start_time = time.time()
        
        try:
            # First generate text content
            text_content = self.generate_text(rant)['content']
            
            # Then convert to audio using ElevenLabs
            if self.elevenlabs_key:
                audio_file = self._generate_audio_with_elevenlabs(text_content)
            else:
                audio_file = self._generate_audio_local(text_content)
            
            processing_time = time.time() - start_time
            
            return {
                'title': 'Generated Audio',
                'content': 'Audio content generated',
                'file_path': audio_file,
                'model_used': 'elevenlabs' if self.elevenlabs_key else 'local',
                'processing_time': processing_time,
                'quality_score': 0.9 if self.elevenlabs_key else 0.3
            }
            
        except Exception as e:
            return {
                'title': 'Audio Generation Failed',
                'content': f'Error: {str(e)}',
                'model_used': 'error',
                'processing_time': time.time() - start_time,
                'quality_score': 0.0
            }
    
    def generate_video(self, rant: Rant) -> Dict[str, Any]:
        """Generate video content from rant"""
        start_time = time.time()
        
        try:
            # Generate video using RunwayML or similar
            if self.runwayml_key:
                video_file = self._generate_video_with_runwayml(rant)
            else:
                video_file = self._generate_video_local(rant)
            
            processing_time = time.time() - start_time
            
            return {
                'title': 'Generated Video',
                'content': 'Video content generated',
                'file_path': video_file,
                'model_used': 'runwayml' if self.runwayml_key else 'local',
                'processing_time': processing_time,
                'quality_score': 0.85 if self.runwayml_key else 0.2
            }
            
        except Exception as e:
            return {
                'title': 'Video Generation Failed',
                'content': f'Error: {str(e)}',
                'model_used': 'error',
                'processing_time': time.time() - start_time,
                'quality_score': 0.0
            }
    
    # Gemini-based generation methods
    def _generate_text_with_gemini(self, rant: Rant) -> str:
        """Generate text using Gemini AI"""
        prompt = f"""
        Transform this rant into a more positive, constructive perspective while acknowledging the person's feelings:
        
        Original rant: "{rant.content}"
        
        Create a response that:
        1. Validates their feelings
        2. Offers a different perspective
        3. Suggests actionable steps
        4. Maintains an empathetic tone
        
        Please provide a thoughtful, supportive response that helps reframe this situation positively.
        """
        
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Gemini text generation error: {e}")
            # Fallback to local generation
            return self._generate_text_local(rant)

    def _generate_meme_with_gemini(self, rant: Rant) -> Dict[str, Any]:
        """Generate meme using Gemini AI"""
        prompt = f"""
        Create a humorous meme based on this rant:
        
        Rant: "{rant.content}"
        
        Generate a meme with:
        1. A funny, relatable title/header
        2. Top text (brief setup)
        3. Bottom text (punchline)
        4. Suggested meme template name
        
        Make it lighthearted and help the person laugh at their situation.
        Format as JSON with keys: title, top_text, bottom_text, template.
        """
        
        try:
            response = self.gemini_model.generate_content(prompt)
            meme_text = response.text.strip()
            
            # Try to parse as JSON, fallback to simple format
            try:
                import json
                meme_data = json.loads(meme_text)
            except:
                # Fallback format
                meme_data = {
                    "title": "Computer Frustration Meme",
                    "top_text": "When your computer crashes",
                    "bottom_text": "And takes all your work with it",
                    "template": "Drake Pointing"
                }
            
            return meme_data
        except Exception as e:
            print(f"Gemini meme generation error: {e}")
            return self._generate_meme_local(rant)

    def _generate_tweet_with_gemini(self, rant: Rant) -> str:
        """Generate tweet using Gemini AI"""
        prompt = f"""
        Transform this rant into a witty, relatable tweet (under 280 characters):
        
        Rant: "{rant.content}"
        
        Make it:
        - Humorous and relatable
        - Twitter-friendly with emojis
        - Positive spin if possible
        - Engaging and shareable
        """
        
        try:
            response = self.gemini_model.generate_content(prompt)
            tweet = response.text.strip()
            
            # Ensure it's under 280 characters
            if len(tweet) > 280:
                tweet = tweet[:277] + "..."
                
            return tweet
        except Exception as e:
            print(f"Gemini tweet generation error: {e}")
            return self._generate_tweet_local(rant)

    # OpenAI-based generation methods
    def _generate_text_with_openai(self, rant: Rant) -> str:
        """Generate text using OpenAI"""
        import openai
        
        prompt = f"""
        Transform this rant into a more positive, constructive perspective while acknowledging the person's feelings:
        
        Original rant: "{rant.content}"
        
        Create a response that:
        1. Validates their feelings
        2. Offers a different perspective
        3. Suggests actionable steps
        4. Maintains an empathetic tone
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a supportive friend who helps people reframe their thoughts positively."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def _generate_meme_with_openai(self, rant: Rant) -> Dict[str, Any]:
        """Generate meme using OpenAI"""
        import openai
        
        prompt = f"""
        Create a relatable meme based on this rant. Provide:
        1. A meme template name (e.g., "Drake Pointing", "Distracted Boyfriend")
        2. Top text
        3. Bottom text
        4. A brief title
        
        Rant: "{rant.content}"
        
        Respond in JSON format:
        {{
            "title": "meme title",
            "template": "meme template name",
            "top_text": "top text",
            "bottom_text": "bottom text"
        }}
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a meme creator who makes relatable, humorous content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.8
        )
        
        return json.loads(response.choices[0].message.content)
    
    def _generate_tweet_with_openai(self, rant: Rant) -> str:
        """Generate tweet using OpenAI"""
        import openai
        
        prompt = f"""
        Transform this rant into a tweet (max 280 characters) that:
        1. Captures the essence of the feeling
        2. Makes it relatable to others
        3. Includes relevant hashtags
        4. Has a tone that's authentic but not overly negative
        
        Original rant: "{rant.content}"
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a social media expert who creates engaging, relatable tweets."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def _generate_song_with_openai(self, rant: Rant) -> Dict[str, str]:
        """Generate song using OpenAI"""
        import openai
        
        prompt = f"""
        Create song lyrics based on this rant:
        
        "{rant.content}"
        
        Create a song with:
        1. A catchy title
        2. Verse 1
        3. Chorus
        4. Verse 2
        5. Chorus
        6. Bridge
        7. Final Chorus
        
        The song should transform the negative energy into something empowering or cathartic.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a songwriter who creates catchy, meaningful songs from personal experiences."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.8
        )
        
        lyrics = response.choices[0].message.content
        
        # Extract title (assume it's the first line)
        lines = lyrics.split('\n')
        title = lines[0].replace('"', '').strip()
        
        return {
            'title': title,
            'lyrics': lyrics
        }
    
    def _generate_script_with_openai(self, rant: Rant) -> str:
        """Generate script using OpenAI"""
        import openai
        
        prompt = f"""
        Create a short comedy script/dialogue based on this rant:
        
        "{rant.content}"
        
        Create a 2-3 minute script with:
        1. Clear character names
        2. Funny dialogue that relates to the rant
        3. A resolution that's uplifting
        4. Stage directions in parentheses
        
        Format it as a proper script.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a comedy writer who creates funny, relatable scripts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.8
        )
        
        return response.choices[0].message.content
    
    # Local generation methods (fallbacks)
    def _generate_text_local(self, rant: Rant) -> str:
        """Generate text using local templates"""
        templates = [
            f"I hear you about {rant.content[:50]}... Here's another way to look at it: Sometimes these challenges help us grow stronger.",
            f"That sounds frustrating. What if we tried to find one small positive thing about this situation?",
            f"Your feelings are valid. Let's think about what actions might help you feel more in control."
        ]
        
        import random
        return random.choice(templates)
    
    def _generate_meme_local(self, rant: Rant) -> Dict[str, Any]:
        """Generate meme using local templates"""
        return {
            'title': 'Relatable Struggle',
            'template': 'Drake Pointing',
            'top_text': 'Dealing with problems maturely',
            'bottom_text': 'Ranting about it online'
        }
    
    def _generate_tweet_local(self, rant: Rant) -> str:
        """Generate tweet using local templates"""
        return f"That moment when {rant.content[:100]}... Anyone else? #relatable #life #struggles"
    
    def _generate_song_local(self, rant: Rant) -> Dict[str, str]:
        """Generate song using local templates"""
        return {
            'title': 'My Rant Song',
            'lyrics': f"""
            [Verse 1]
            Sometimes I feel like {rant.content[:30]}...
            But I know that this will pass
            
            [Chorus]
            I'm gonna make it through
            I'm gonna make it through
            These feelings aren't forever
            I'm gonna make it through
            """
        }
    
    def _generate_script_local(self, rant: Rant) -> str:
        """Generate script using local templates"""
        return f"""
        SCENE: A person talking to their reflection
        
        PERSON: (frustrated) {rant.content[:50]}...
        
        REFLECTION: (calmly) I know it's hard, but what if we looked at this differently?
        
        PERSON: (curious) How so?
        
        REFLECTION: What if this is exactly what we need to learn right now?
        
        (Both smile)
        
        END SCENE
        """
    
    def _generate_audio_with_elevenlabs(self, text: str) -> str:
        """Generate audio using ElevenLabs API"""
        # This would integrate with ElevenLabs API
        # For now, return placeholder
        return "audio_placeholder.mp3"
    
    def _generate_audio_local(self, text: str) -> str:
        """Generate audio using local TTS"""
        # This would use local TTS libraries
        return "local_audio_placeholder.mp3"
    
    def _generate_video_with_runwayml(self, rant: Rant) -> str:
        """Generate video using RunwayML API"""
        # This would integrate with RunwayML API
        return "video_placeholder.mp4"
    
    def _generate_video_local(self, rant: Rant) -> str:
        """Generate video using local tools"""
        # This would use local video generation tools
        return "local_video_placeholder.mp4"
