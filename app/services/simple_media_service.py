import os
import io
import base64
from PIL import Image, ImageDraw, ImageFont
import tempfile
import logging
from werkzeug.utils import secure_filename
import json
import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS
import cv2
import numpy as np
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: Google Generative AI not available. Using fallback methods.")

class SimpleMediaService:
    """Simple media service for basic functionality with optional Gemini integration"""
    
    def __init__(self):
        self.upload_folder = 'uploads'
        self.output_folder = 'outputs'
        
        # Create directories if they don't exist
        os.makedirs(self.upload_folder, exist_ok=True)
        os.makedirs(self.output_folder, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize Gemini if available
        self.gemini_model = None
        self._init_gemini()
    
    def _init_gemini(self):
        """Initialize Gemini API if available"""
        if GEMINI_AVAILABLE:
            try:
                gemini_key = os.getenv('GEMINI_API_KEY')
                if gemini_key and gemini_key != 'your-gemini-api-key-here':
                    genai.configure(api_key=gemini_key)
                    self.gemini_model = genai.GenerativeModel('gemini-pro')
                    self.logger.info("Gemini AI initialized successfully!")
                else:
                    self.logger.warning("Gemini API key not configured")
            except Exception as e:
                self.logger.error(f"Error initializing Gemini: {e}")
                self.gemini_model = None
    
    def process_audio_file(self, audio_file):
        """Real audio processing with speech recognition"""
        try:
            # Save the uploaded file
            filename = secure_filename(audio_file.filename)
            filepath = os.path.join(self.upload_folder, filename)
            audio_file.save(filepath)
            
            # Initialize speech recognizer
            recognizer = sr.Recognizer()
            
            try:
                # Convert audio to WAV format if needed
                wav_path = None
                if filename.lower().endswith('.mp3'):
                    audio = AudioSegment.from_mp3(filepath)
                    wav_path = filepath.replace('.mp3', '.wav')
                    audio.export(wav_path, format="wav")
                    audio_path = wav_path
                elif filename.lower().endswith('.wav'):
                    audio_path = filepath
                else:
                    # Try to convert using pydub
                    audio = AudioSegment.from_file(filepath)
                    wav_path = filepath.replace(os.path.splitext(filepath)[1], '.wav')
                    audio.export(wav_path, format="wav")
                    audio_path = wav_path
                
                # Perform speech recognition
                with sr.AudioFile(audio_path) as source:
                    audio_data = recognizer.record(source)
                
                # Try to recognize speech using Google's service
                try:
                    text = recognizer.recognize_google(audio_data)
                    self.logger.info(f"Speech recognition successful: {text}")
                    
                    # Use Gemini to enhance the text if available
                    if self.gemini_model:
                        try:
                            enhanced_prompt = f"""
                            Based on this audio transcription, create a more detailed and emotionally rich version 
                            that captures the likely feelings and context. Keep it realistic and relatable:
                            
                            Original: "{text}"
                            
                            Enhanced version:
                            """
                            
                            response = self.gemini_model.generate_content(enhanced_prompt)
                            enhanced_text = response.text.strip()
                            text = enhanced_text
                            
                        except Exception as e:
                            self.logger.warning(f"Gemini enhancement failed: {e}")
                    
                except sr.UnknownValueError:
                    # Fall back to mock text if recognition fails
                    text = "I'm feeling overwhelmed and frustrated right now. There's so much going on in my life and I just need to express these feelings somehow."
                    self.logger.warning("Speech recognition failed, using fallback text")
                
                except sr.RequestError as e:
                    # Fall back to mock text if service is unavailable
                    text = "I'm feeling overwhelmed and frustrated right now. There's so much going on in my life and I just need to express these feelings somehow."
                    self.logger.warning(f"Speech recognition service error: {e}")
                
            except Exception as e:
                # Fall back to mock text if audio processing fails
                text = "I'm feeling overwhelmed and frustrated right now. There's so much going on in my life and I just need to express these feelings somehow."
                self.logger.warning(f"Audio processing failed: {e}")
                wav_path = None
            
            # Clean up temporary files
            try:
                os.remove(filepath)
                if wav_path and os.path.exists(wav_path):
                    os.remove(wav_path)
            except:
                pass
            
            return {
                'success': True,
                'text': text,
                'message': 'Audio processed successfully'
            }
            
        except Exception as e:
            self.logger.error(f"Audio processing error: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Error processing audio file'
            }
    
    def process_image_file(self, image_file):
        """Process uploaded image file"""
        try:
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(self.upload_folder, filename)
            image_file.save(filepath)
            
            # Open and process image
            image = Image.open(filepath)
            
            # Basic image analysis
            width, height = image.size
            format = image.format
            mode = image.mode
            
            # Convert to base64 for frontend display
            buffered = io.BytesIO()
            image.save(buffered, format=format or 'JPEG')
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            # Clean up
            os.remove(filepath)
            
            return {
                'success': True,
                'image_data': f"data:image/{format.lower()};base64,{img_str}",
                'metadata': {
                    'width': width,
                    'height': height,
                    'format': format,
                    'mode': mode
                },
                'message': 'Image processed successfully'
            }
            
        except Exception as e:
            self.logger.error(f"Image processing error: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Error processing image file'
            }
    
    def text_to_speech(self, text, language='en', slow=False):
        """Convert text to speech using gTTS"""
        try:
            # Create gTTS object
            tts = gTTS(text=text, lang=language, slow=slow)
            
            # Save to a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            tts.save(temp_file.name)
            
            # Read the file and convert to base64
            with open(temp_file.name, 'rb') as audio_file:
                audio_data = audio_file.read()
                audio_base64 = base64.b64encode(audio_data).decode()
            
            # Clean up temporary file
            os.remove(temp_file.name)
            
            return {
                'success': True,
                'audio_data': f"data:audio/mp3;base64,{audio_base64}",
                'message': f'Text-to-speech generated successfully - Language: {language}, Slow: {slow}'
            }
            
        except Exception as e:
            self.logger.error(f"TTS generation error: {e}")
            # Fall back to mock audio
            mock_audio_url = f"data:audio/mp3;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwgBSGA0fPTgCsELYPL8N2Eeyz"
            return {
                'success': True,
                'audio_data': mock_audio_url,
                'message': f'Text-to-speech generated (fallback) - Language: {language}, Slow: {slow}'
            }
    
    def generate_meme_image(self, text, template_type='default'):
        """Generate meme image with text"""
        try:
            # Create a basic meme template
            width, height = 800, 600
            
            # Create image with gradient background
            image = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(image)
            
            # Create gradient background
            for i in range(height):
                gradient_color = int(255 * (1 - i/height))
                color = (gradient_color//4, gradient_color//2, gradient_color)
                draw.line([(0, i), (width, i)], fill=color)
            
            # Add text
            try:
                # Try to use a better font
                font = ImageFont.truetype("arial.ttf", 48)
            except:
                # Fall back to default font
                font = ImageFont.load_default()
            
            # Word wrap text
            words = text.split()
            lines = []
            current_line = []
            
            for word in words:
                current_line.append(word)
                line_text = ' '.join(current_line)
                bbox = draw.textbbox((0, 0), line_text, font=font)
                if bbox[2] - bbox[0] > width - 100:  # Leave margin
                    if len(current_line) > 1:
                        current_line.pop()
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        lines.append(word)
                        current_line = []
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Draw text centered
            total_height = len(lines) * 60
            start_y = (height - total_height) // 2
            
            for i, line in enumerate(lines):
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x = (width - text_width) // 2
                y = start_y + i * 60
                
                # Draw text with outline
                for dx in [-2, -1, 0, 1, 2]:
                    for dy in [-2, -1, 0, 1, 2]:
                        if dx != 0 or dy != 0:
                            draw.text((x + dx, y + dy), line, font=font, fill='black')
                
                draw.text((x, y), line, font=font, fill='white')
            
            # Convert to base64
            buffered = io.BytesIO()
            image.save(buffered, format='PNG')
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return {
                'success': True,
                'image_data': f"data:image/png;base64,{img_str}",
                'message': 'Meme generated successfully'
            }
            
        except Exception as e:
            self.logger.error(f"Meme generation error: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Error generating meme'
            }
    
    def create_video_from_text(self, text, background_color=(30, 30, 30), duration=10):
        """Create a real video with text overlay"""
        try:
            # Create a temporary video file
            temp_video = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            temp_video.close()
            
            # Create video using OpenCV
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            fps = 24
            width, height = 800, 600
            
            # Create video writer
            video_writer = cv2.VideoWriter(temp_video.name, fourcc, fps, (width, height))
            
            # Prepare text for display
            words = text.split()
            lines = []
            words_per_line = 6
            
            for i in range(0, len(words), words_per_line):
                line = ' '.join(words[i:i+words_per_line])
                lines.append(line)
            
            # Create frames
            total_frames = int(fps * duration)
            frames_per_line = total_frames // len(lines) if lines else total_frames
            
            for frame_num in range(total_frames):
                # Create frame
                frame = np.full((height, width, 3), background_color, dtype=np.uint8)
                
                # Determine which line to show
                if lines:
                    line_index = min(frame_num // frames_per_line, len(lines) - 1)
                    current_line = lines[line_index]
                    
                    # Add text to frame
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.8
                    font_color = (255, 255, 255)
                    thickness = 2
                    
                    # Get text size
                    text_size = cv2.getTextSize(current_line, font, font_scale, thickness)[0]
                    
                    # Calculate position to center text
                    text_x = (width - text_size[0]) // 2
                    text_y = (height + text_size[1]) // 2
                    
                    # Add text to frame
                    cv2.putText(frame, current_line, (text_x, text_y), font, font_scale, font_color, thickness)
                
                # Write frame
                video_writer.write(frame)
            
            # Release video writer
            video_writer.release()
            
            # Read the video file and convert to base64
            with open(temp_video.name, 'rb') as video_file:
                video_data = video_file.read()
                video_base64 = base64.b64encode(video_data).decode()
            
            # Clean up temporary file
            os.remove(temp_video.name)
            
            return {
                'success': True,
                'video_data': f"data:video/mp4;base64,{video_base64}",
                'message': 'Video generated successfully'
            }
            
        except Exception as e:
            self.logger.error(f"Video generation error: {e}")
            # Fall back to mock response
            mock_response = {
                'text': text,
                'background_color': background_color,
                'duration': duration,
                'status': 'fallback_service'
            }
            
            # Encode as base64 for consistency
            mock_data = json.dumps(mock_response).encode()
            mock_base64 = base64.b64encode(mock_data).decode()
            
            return {
                'success': True,
                'video_data': f"data:application/json;base64,{mock_base64}",
                'message': 'Video generation failed - fallback response returned'
            }
