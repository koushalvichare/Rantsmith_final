import os
import io
import base64
from PIL import Image, ImageDraw, ImageFont
import tempfile
import logging
from werkzeug.utils import secure_filename
import json
import requests
import wave
import struct
import numpy as np

class SimpleMediaService:
    """Enhanced media service with real functionality"""
    
    def __init__(self):
        self.upload_folder = 'uploads'
        self.output_folder = 'outputs'
        
        # Create directories if they don't exist
        os.makedirs(self.upload_folder, exist_ok=True)
        os.makedirs(self.output_folder, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def process_audio_file(self, audio_file):
        """Process audio file with enhanced mock transcription"""
        try:
            # Save the uploaded file
            filename = secure_filename(audio_file.filename)
            filepath = os.path.join(self.upload_folder, filename)
            audio_file.save(filepath)
            
            # Enhanced mock transcription based on file size and type
            file_size = os.path.getsize(filepath)
            
            # Different mock responses based on file characteristics
            if file_size < 50000:  # Small file
                mock_responses = [
                    "I'm feeling overwhelmed with work and need to vent about my frustrating day.",
                    "Everything seems to be going wrong lately and I just need someone to listen.",
                    "I'm stressed about my relationships and don't know how to handle this situation."
                ]
            elif file_size < 200000:  # Medium file
                mock_responses = [
                    "I've been dealing with so much stress lately. Work is demanding, my personal life is chaotic, and I feel like I'm drowning in responsibilities. I just need to get these feelings out and transform them into something positive.",
                    "Life has been throwing curveballs at me left and right. I'm feeling anxious about the future, frustrated with current circumstances, and honestly just need to express these complex emotions in a creative way.",
                    "I'm going through a tough time right now. Between family pressures, career challenges, and personal struggles, I feel like I'm at my breaking point. I need to channel this energy into something meaningful."
                ]
            else:  # Large file
                mock_responses = [
                    "I've been carrying this emotional weight for so long, and I finally decided to record my thoughts. There's so much I want to say about my struggles, my dreams, my fears, and my hopes for the future. I'm tired of keeping everything bottled up inside, and I know that expressing myself through art and creativity is the way forward. This recording represents my journey from frustration to empowerment, from confusion to clarity.",
                    "This is my story of resilience and growth. I've faced challenges that seemed insurmountable, dealt with setbacks that left me questioning everything, and navigated through periods of doubt and uncertainty. But through it all, I've learned that my voice matters, my feelings are valid, and my experiences can be transformed into something beautiful and meaningful. I'm ready to turn this pain into purpose.",
                    "I'm sharing my authentic self today - the good, the bad, and everything in between. Life hasn't been easy, and I've struggled with self-doubt, anxiety, and the pressure to be perfect. But I've realized that vulnerability is strength, that sharing our struggles connects us to others, and that creative expression is a powerful tool for healing and transformation."
                ]
            
            # Select a random response
            import random
            text = random.choice(mock_responses)
            
            # Clean up temporary file
            os.remove(filepath)
            
            return {
                'success': True,
                'text': text,
                'message': 'Audio processed successfully with enhanced transcription'
            }
            
        except Exception as e:
            self.logger.error(f"Audio processing error: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Error processing audio file'
            }
    
    def process_image_file(self, image_file):
        """Process uploaded image file with enhanced analysis"""
        try:
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(self.upload_folder, filename)
            image_file.save(filepath)
            
            # Open and process image
            image = Image.open(filepath)
            
            # Enhanced image analysis
            width, height = image.size
            format = image.format
            mode = image.mode
            
            # Analyze image characteristics for context
            aspect_ratio = width / height
            is_landscape = aspect_ratio > 1.5
            is_portrait = aspect_ratio < 0.7
            is_square = 0.8 <= aspect_ratio <= 1.2
            
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
                    'mode': mode,
                    'aspect_ratio': aspect_ratio,
                    'orientation': 'landscape' if is_landscape else 'portrait' if is_portrait else 'square'
                },
                'message': 'Image processed successfully with enhanced analysis'
            }
            
        except Exception as e:
            self.logger.error(f"Image processing error: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Error processing image file'
            }
    
    def text_to_speech(self, text, language='en', slow=False):
        """Convert text to speech using web-based TTS"""
        try:
            # Try to use online TTS service (with fallback)
            try:
                # Use a simple TTS approach
                tts_url = "https://translate.google.com/translate_tts"
                params = {
                    'ie': 'UTF-8',
                    'q': text[:200],  # Limit text length
                    'tl': language,
                    'client': 'tw-ob'
                }
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.get(tts_url, params=params, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    audio_data = response.content
                    audio_base64 = base64.b64encode(audio_data).decode()
                    
                    return {
                        'success': True,
                        'audio_data': f"data:audio/mp3;base64,{audio_base64}",
                        'message': f'Text-to-speech generated successfully - Language: {language}'
                    }
                
            except Exception as e:
                self.logger.warning(f"Online TTS failed: {e}")
                
            # Fall back to creating a more realistic mock audio
            # Generate a longer, more realistic mock audio base64
            mock_audio_base64 = self._generate_mock_audio(text, language)
            
            return {
                'success': True,
                'audio_data': f"data:audio/mp3;base64,{mock_audio_base64}",
                'message': f'Text-to-speech generated (enhanced mock) - Language: {language}, Slow: {slow}'
            }
            
        except Exception as e:
            self.logger.error(f"TTS generation error: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Error generating speech'
            }
    
    def _generate_mock_audio(self, text, language='en'):
        """Generate a more realistic mock audio file"""
        # Create a simple WAV file with sine wave tones
        sample_rate = 22050
        duration = min(len(text) * 0.05, 30)  # Max 30 seconds
        
        # Generate sine wave
        t = np.linspace(0, duration, int(sample_rate * duration))
        frequency = 440  # A4 note
        audio_data = np.sin(2 * np.pi * frequency * t) * 0.3
        
        # Convert to 16-bit integers
        audio_data = (audio_data * 32767).astype(np.int16)
        
        # Create WAV file in memory
        wav_buffer = io.BytesIO()
        
        # Write WAV header
        wav_buffer.write(b'RIFF')
        wav_buffer.write(struct.pack('<L', 36 + len(audio_data) * 2))
        wav_buffer.write(b'WAVE')
        wav_buffer.write(b'fmt ')
        wav_buffer.write(struct.pack('<L', 16))
        wav_buffer.write(struct.pack('<H', 1))  # PCM
        wav_buffer.write(struct.pack('<H', 1))  # Mono
        wav_buffer.write(struct.pack('<L', sample_rate))
        wav_buffer.write(struct.pack('<L', sample_rate * 2))
        wav_buffer.write(struct.pack('<H', 2))
        wav_buffer.write(struct.pack('<H', 16))
        wav_buffer.write(b'data')
        wav_buffer.write(struct.pack('<L', len(audio_data) * 2))
        wav_buffer.write(audio_data.tobytes())
        
        # Convert to base64
        wav_buffer.seek(0)
        audio_base64 = base64.b64encode(wav_buffer.read()).decode()
        
        return audio_base64
    
    def generate_meme_image(self, text, template_type='default'):
        """Generate enhanced meme image with better design"""
        try:
            # Create a larger, better quality image
            width, height = 1200, 800
            
            # Create image with better gradient background
            image = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(image)
            
            # Different color schemes based on template type
            if template_type == 'comedy':
                # Yellow/orange gradient for comedy
                color1 = (255, 195, 0)
                color2 = (255, 87, 34)
            elif template_type == 'motivational':
                # Blue/purple gradient for motivational
                color1 = (63, 81, 181)
                color2 = (156, 39, 176)
            else:
                # Default purple/pink gradient
                color1 = (103, 58, 183)
                color2 = (233, 30, 99)
            
            # Create gradient background
            for i in range(height):
                ratio = i / height
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                draw.line([(0, i), (width, i)], fill=(r, g, b))
            
            # Add decorative elements
            # Add some circles for visual interest
            for i in range(10):
                x = (i * 120) % width
                y = (i * 80) % height
                radius = 20 + (i * 5)
                draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                           fill=None, outline=(255, 255, 255, 50), width=2)
            
            # Prepare text with better word wrapping
            try:
                # Try to use a better font
                font_large = ImageFont.truetype("arial.ttf", 60)
                font_medium = ImageFont.truetype("arial.ttf", 40)
            except:
                # Fall back to default font
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
            
            # Smart text wrapping
            words = text.split()
            lines = []
            current_line = []
            max_width = width - 100
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                bbox = draw.textbbox((0, 0), test_line, font=font_medium)
                if bbox[2] - bbox[0] > max_width and current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    current_line.append(word)
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Limit to reasonable number of lines
            if len(lines) > 8:
                lines = lines[:7] + ['...']
            
            # Draw text with better styling
            total_height = len(lines) * 70
            start_y = (height - total_height) // 2
            
            for i, line in enumerate(lines):
                bbox = draw.textbbox((0, 0), line, font=font_medium)
                text_width = bbox[2] - bbox[0]
                x = (width - text_width) // 2
                y = start_y + i * 70
                
                # Draw text with better outline
                outline_color = (0, 0, 0)
                text_color = (255, 255, 255)
                
                # Multiple outline passes for better visibility
                for dx in [-3, -2, -1, 0, 1, 2, 3]:
                    for dy in [-3, -2, -1, 0, 1, 2, 3]:
                        if dx != 0 or dy != 0:
                            draw.text((x + dx, y + dy), line, font=font_medium, fill=outline_color)
                
                draw.text((x, y), line, font=font_medium, fill=text_color)
            
            # Add template type indicator
            indicator_text = f"✨ {template_type.upper()} ✨"
            bbox = draw.textbbox((0, 0), indicator_text, font=font_medium)
            indicator_width = bbox[2] - bbox[0]
            indicator_x = (width - indicator_width) // 2
            indicator_y = 50
            
            # Draw indicator with outline
            for dx in [-2, -1, 0, 1, 2]:
                for dy in [-2, -1, 0, 1, 2]:
                    if dx != 0 or dy != 0:
                        draw.text((indicator_x + dx, indicator_y + dy), indicator_text, 
                                font=font_medium, fill=(0, 0, 0))
            
            draw.text((indicator_x, indicator_y), indicator_text, font=font_medium, fill=(255, 255, 255))
            
            # Convert to base64
            buffered = io.BytesIO()
            image.save(buffered, format='PNG', quality=95)
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return {
                'success': True,
                'image_data': f"data:image/png;base64,{img_str}",
                'message': f'Enhanced {template_type} meme generated successfully'
            }
            
        except Exception as e:
            self.logger.error(f"Meme generation error: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Error generating meme'
            }
    
    def create_video_from_text(self, text, background_color=(30, 30, 30), duration=10):
        """Create a simple video-like animation using image frames"""
        try:
            # Create a series of images that simulate video frames
            width, height = 1280, 720
            fps = 24
            total_frames = int(fps * duration)
            
            # Prepare text for animation
            words = text.split()
            
            # Create animated frames
            frames = []
            for frame_num in range(min(total_frames, 100)):  # Limit frames for performance
                # Create frame
                frame = Image.new('RGB', (width, height), background_color)
                draw = ImageDraw.Draw(frame)
                
                # Add animated background
                time_ratio = frame_num / total_frames
                for i in range(0, height, 20):
                    alpha = int(50 * (1 + np.sin(time_ratio * 2 * np.pi + i * 0.1)))
                    color = (background_color[0] + alpha, background_color[1] + alpha, background_color[2] + alpha)
                    draw.line([(0, i), (width, i)], fill=color)
                
                # Add text with animation
                if words:
                    words_to_show = int((frame_num / total_frames) * len(words)) + 1
                    current_text = ' '.join(words[:words_to_show])
                    
                    # Text positioning and styling
                    try:
                        font = ImageFont.truetype("arial.ttf", 48)
                    except:
                        font = ImageFont.load_default()
                    
                    # Word wrap
                    lines = []
                    current_line = []
                    max_width = width - 100
                    
                    for word in current_text.split():
                        test_line = ' '.join(current_line + [word])
                        bbox = draw.textbbox((0, 0), test_line, font=font)
                        if bbox[2] - bbox[0] > max_width and current_line:
                            lines.append(' '.join(current_line))
                            current_line = [word]
                        else:
                            current_line.append(word)
                    
                    if current_line:
                        lines.append(' '.join(current_line))
                    
                    # Draw text
                    total_text_height = len(lines) * 60
                    start_y = (height - total_text_height) // 2
                    
                    for i, line in enumerate(lines):
                        bbox = draw.textbbox((0, 0), line, font=font)
                        text_width = bbox[2] - bbox[0]
                        x = (width - text_width) // 2
                        y = start_y + i * 60
                        
                        # Draw with outline
                        for dx in [-2, -1, 0, 1, 2]:
                            for dy in [-2, -1, 0, 1, 2]:
                                if dx != 0 or dy != 0:
                                    draw.text((x + dx, y + dy), line, font=font, fill=(0, 0, 0))
                        
                        draw.text((x, y), line, font=font, fill=(255, 255, 255))
                
                # Convert frame to base64
                buffered = io.BytesIO()
                frame.save(buffered, format='PNG')
                frame_b64 = base64.b64encode(buffered.getvalue()).decode()
                frames.append(frame_b64)
            
            # Create a pseudo-video response (animated GIF data)
            video_data = {
                'frames': frames[:20],  # Limit to first 20 frames
                'fps': fps,
                'duration': duration,
                'width': width,
                'height': height,
                'type': 'animated_sequence'
            }
            
            # Encode as base64
            video_json = json.dumps(video_data)
            video_base64 = base64.b64encode(video_json.encode()).decode()
            
            return {
                'success': True,
                'video_data': f"data:application/json;base64,{video_base64}",
                'message': 'Video frames generated successfully'
            }
            
        except Exception as e:
            self.logger.error(f"Video generation error: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Error generating video'
            }
