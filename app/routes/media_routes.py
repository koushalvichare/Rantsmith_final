from flask_login import current_user
from flask import Blueprint, request, jsonify
from app.services.professional_media_service import ProfessionalMediaService
from app.models import Rant, GeneratedContent, ContentType, User
from app import db
import logging
import jwt
from flask import current_app
from functools import wraps

# JWT Authentication decorator
def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'error': 'No token provided'}), 401
            
            # Remove 'Bearer ' prefix
            if token.startswith('Bearer '):
                token = token[7:]
            
            # Verify token
            try:
                payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
                user_id = payload['user_id']
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token has expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Invalid token'}), 401
            
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Add user to request context
            # request.current_user = user  # Not needed, use flask_login.current_user
            return f(*args, **kwargs)
            
        except Exception as e:
            logging.error(f"JWT auth error: {e}")
            return jsonify({'error': 'Authentication failed'}), 401
    
    return decorated_function

media_bp = Blueprint('media', __name__)

@media_bp.route('/test', methods=['GET'])
def test_media_endpoint():
    """Test endpoint to check if media routes are working"""
    return jsonify({
        'message': 'Media API is working!',
        'endpoints': [
            '/api/media/upload-audio',
            '/api/media/upload-image',
            '/api/media/generate-speech',
            '/api/media/generate-meme',
            '/api/media/generate-video',
            '/api/media/transform-with-ai'
        ]
    })

@media_bp.route('/upload-audio', methods=['POST'])
@jwt_required
def upload_audio():
    """Handle audio file upload and convert to text"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Process audio file
        media_service = ProfessionalMediaService()
        result = media_service.process_audio_file(audio_file)
        
        if result['success']:
            # Create a new rant from the transcribed text
            rant = Rant(
                user_id=current_user.id,
                content=result['text'],
                input_type='audio',
                processed=False
            )
            db.session.add(rant)
            db.session.commit()
            
            return jsonify({
                'message': 'Audio processed successfully',
                'text': result['text'],
                'rant_id': rant.id
            }), 200
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        logging.error(f"Audio upload error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@media_bp.route('/upload-image', methods=['POST'])
@jwt_required
def upload_image():
    """Handle image file upload and processing"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Process image file
        media_service = ProfessionalMediaService()
        result = media_service.process_image_file(image_file)
        
        if result['success']:
            return jsonify({
                'message': 'Image processed successfully',
                'image_data': result['image_data'],
                'metadata': result['metadata']
            }), 200
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        logging.error(f"Image upload error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@media_bp.route('/generate-speech/<int:rant_id>', methods=['POST'])
@jwt_required
def generate_speech(rant_id):
    """Generate speech from rant text"""
    try:
        rant = Rant.query.filter_by(id=rant_id, user_id=current_user.id).first()
        if not rant:
            return jsonify({'error': 'Rant not found'}), 404
        
        data = request.get_json() or {}
        language = data.get('language', 'en')
        slow = data.get('slow', False)
        
        # Generate speech
        media_service = ProfessionalMediaService()
        result = media_service.text_to_speech(rant.content, rant.transformation_type, language)
        
        if result['success']:
            return jsonify({
                'message': 'Speech generated successfully',
                'audio_data': result['audio_data']
            }), 200
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        logging.error(f"Speech generation error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@media_bp.route('/generate-meme/<int:rant_id>', methods=['POST'])
@jwt_required
def generate_meme(rant_id):
    """Generate meme from rant text"""
    try:
        rant = Rant.query.filter_by(id=rant_id, user_id=current_user.id).first()
        if not rant:
            return jsonify({'error': 'Rant not found'}), 404
        
        data = request.get_json() or {}
        template_type = data.get('template_type', 'default')
        
        # Generate meme
        media_service = ProfessionalMediaService()
        result = media_service.generate_meme_image(rant.content, template_type)
        
        if result['success']:
            return jsonify({
                'message': 'Meme generated successfully',
                'image_data': result['image_data']
            }), 200
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        logging.error(f"Meme generation error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@media_bp.route('/generate-video/<int:rant_id>', methods=['POST'])
@jwt_required
def generate_video(rant_id):
    """Generate video from rant text"""
    try:
        rant = Rant.query.filter_by(id=rant_id, user_id=current_user.id).first()
        if not rant:
            return jsonify({'error': 'Rant not found'}), 404
        
        data = request.get_json() or {}
        duration = data.get('duration', 10)
        background_color = data.get('background_color', [30, 30, 30])
        
        # Generate video
        media_service = ProfessionalMediaService()
        result = media_service.create_video_from_text(rant.content, tuple(background_color), duration)
        
        if result['success']:
            return jsonify({
                'message': 'Video generated successfully',
                'video_data': result['video_data']
            }), 200
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        logging.error(f"Video generation error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@media_bp.route('/transform-with-ai/<int:rant_id>', methods=['POST'])
@jwt_required
def transform_with_ai(rant_id):
    """Transform rant content and generate text output"""
    try:
        rant = Rant.query.filter_by(id=rant_id, user_id=current_user.id).first()
        if not rant:
            return jsonify({'error': 'Rant not found'}), 404
        
        data = request.get_json() or {}
        transformation_type = data.get('transformation_type', 'poem')
        output_format = data.get('output_format', 'text')
        
        # Simple transformation based on type
        original_content = rant.content
        
        if transformation_type == 'poem':
            lines = original_content.split('.')
            transformed_text = '\n'.join([f"In feelings deep, {line.strip()}," for line in lines[:4] if line.strip()])
            transformed_text += f"\n\nTransformed from: {original_content[:50]}..."
        elif transformation_type == 'song':
            transformed_text = f"[Verse 1]\n{original_content[:100]}...\n\n[Chorus]\nEvery feeling has its place\nIn this song of life and grace"
        elif transformation_type == 'story':
            transformed_text = f"Once upon a time, someone felt exactly like this: {original_content}\n\nAnd they lived happily ever after, knowing their feelings were valid."
        elif transformation_type == 'motivational':
            transformed_text = f"Remember this: {original_content}\n\nBut also remember - you are stronger than you know, and this too shall pass. Every challenge is an opportunity to grow."
        else:
            transformed_text = f"Transformed ({transformation_type}): {original_content}"
        
        # Mark rant as processed
        rant.processed = True
        db.session.commit()
        
        return jsonify({
            'message': 'Content transformed successfully',
            'transformation_type': transformation_type,
            'output_format': output_format,
            'text': transformed_text
        }), 200
        
    except Exception as e:
        logging.error(f"AI transformation error: {e}")
        return jsonify({'error': 'Internal server error'}), 500
