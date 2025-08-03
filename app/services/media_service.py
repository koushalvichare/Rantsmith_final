import os
import io
import base64
from PIL import Image, ImageDraw, ImageFont
import tempfile
import logging
from werkzeug.utils import secure_filename
import numpy as np

# Optional imports with fallbacks
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    sr = None

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    gTTS = None

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    pygame = None

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    AudioSegment = None

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    cv2 = None

class MediaService:
    """Service for handling audio and image processing"""
    
    def __init__(self):
        if SPEECH_RECOGNITION_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
        else:
            self.recognizer = None
            self.microphone = None
            
        self.upload_folder = 'uploads'
        self.output_folder = 'outputs'
        
        # Create directories if they don't exist
        os.makedirs(self.upload_folder, exist_ok=True)
        os.makedirs(self.output_folder, exist_ok=True)
        
        # Initialize pygame mixer for audio playback
        if PYGAME_AVAILABLE:
            pygame.mixer.init()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def process_audio_file(self, audio_file):
        """Process uploaded audio file and convert to text"""
        if not SPEECH_RECOGNITION_AVAILABLE:
            return {
                'success': False,
                'error': 'Speech recognition not available',
                'message': 'Speech recognition dependencies not installed'
            }
            
        try:
            # Save the uploaded file
            filename = secure_filename(audio_file.filename)
            filepath = os.path.join(self.upload_folder, filename)
            audio_file.save(filepath)
            
            # Convert to text using speech recognition
            with sr.AudioFile(filepath) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data)
                
            # Clean up temporary file
            os.remove(filepath)
            
            return {
                'success': True,
                'text': text,
                'message': 'Audio processed successfully'
            }
            
        except sr.UnknownValueError:
            return {
                'success': False,
                'error': 'Could not understand audio',
                'message': 'Please try speaking more clearly'
            }
        except sr.RequestError as e:
            return {
                'success': False,
                'error': f'Error with speech recognition service: {e}',
                'message': 'Speech recognition service is unavailable'
            }
        except Exception as e:
            self.logger.error(f"Audio processing error: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Error processing audio file'
            }
    
    def process_image_file(self, image_file):
        """Process uploaded image file and extract text if any"""
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
        """Convert text to speech and return audio file"""
        if not GTTS_AVAILABLE:
            return {
                'success': False,
                'error': 'Text-to-speech not available',
                'message': 'gTTS dependencies not installed'
            }
            
        try:
            # Create TTS object
            tts = gTTS(text=text, lang=language, slow=slow)
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            tts.save(temp_file.name)
            
            # Read the file and convert to base64
            with open(temp_file.name, 'rb') as f:
                audio_data = f.read()
                audio_base64 = base64.b64encode(audio_data).decode()
            
            # Clean up
            os.unlink(temp_file.name)
            
            return {
                'success': True,
                'audio_data': f"data:audio/mp3;base64,{audio_base64}",
                'message': 'Text converted to speech successfully'
            }
            
        except Exception as e:
            self.logger.error(f"Text-to-speech error: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Error converting text to speech'
            }
    
    def generate_meme_image(self, text, template_type='default'):
        """Generate meme image with text"""
        try:
            # Create a basic meme template
            width, height = 800, 600
            
            # Create image with gradient background
            image = Image.new('RGB', (width, height), color='#1a1a1a')
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
        """Create a simple video with text overlay"""
        if not OPENCV_AVAILABLE:
            return {
                'success': False,
                'error': 'Video creation not available',
                'message': 'OpenCV dependencies not installed'
            }
            
        try:
            # Create a video frame
            width, height = 1280, 720
            fps = 30
            
            # Create temporary video file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            temp_file.close()
            
            # Create video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(temp_file.name, fourcc, fps, (width, height))
            
            # Generate frames
            for frame_num in range(duration * fps):
                # Create frame
                frame = np.zeros((height, width, 3), dtype=np.uint8)
                frame[:] = background_color
                
                # Add text
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1.5
                thickness = 2
                
                # Word wrap
                words = text.split()
                lines = []
                current_line = []
                
                for word in words:
                    test_line = ' '.join(current_line + [word])
                    (test_width, test_height), _ = cv2.getTextSize(test_line, font, font_scale, thickness)
                    
                    if test_width > width - 100:
                        if current_line:
                            lines.append(' '.join(current_line))
                            current_line = [word]
                        else:
                            lines.append(word)
                    else:
                        current_line.append(word)
                
                if current_line:
                    lines.append(' '.join(current_line))
                
                # Draw text
                line_height = 50
                start_y = (height - len(lines) * line_height) // 2
                
                for i, line in enumerate(lines):
                    (text_width, text_height), _ = cv2.getTextSize(line, font, font_scale, thickness)
                    x = (width - text_width) // 2
                    y = start_y + i * line_height + text_height
                    
                    cv2.putText(frame, line, (x, y), font, font_scale, (255, 255, 255), thickness)
                
                out.write(frame)
            
            out.release()
            
            # Read video file and convert to base64
            with open(temp_file.name, 'rb') as f:
                video_data = f.read()
                video_base64 = base64.b64encode(video_data).decode()
            
            # Clean up
            os.unlink(temp_file.name)
            
            return {
                'success': True,
                'video_data': f"data:video/mp4;base64,{video_base64}",
                'message': 'Video generated successfully'
            }
            
        except Exception as e:
            self.logger.error(f"Video generation error: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Error generating video'
            }
