from flask import Blueprint, request, jsonify, current_app
from app.services.simple_media_service import SimpleMediaService
from app.models import Rant, GeneratedContent, ContentType, User
from app import db
from app.utils.auth import jwt_required, get_current_user
import logging

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
        media_service = SimpleMediaService()
        result = media_service.process_audio_file(audio_file)
        
        if result['success']:
            # Create a new rant from the transcribed text
            current_user = get_current_user()
            if not current_user:
                return jsonify({'error': 'User not authenticated'}), 401
                
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
        media_service = SimpleMediaService()
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
        current_user = get_current_user()
        if not current_user:
            return jsonify({'error': 'User not authenticated'}), 401
            
        rant = Rant.query.filter_by(id=rant_id, user_id=current_user.id).first()
        if not rant:
            return jsonify({'error': 'Rant not found'}), 404
        
        data = request.get_json() or {}
        language = data.get('language', 'en')
        slow = data.get('slow', False)
        
        # Generate speech
        media_service = SimpleMediaService()
        result = media_service.text_to_speech(rant.content, language, slow)
        
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
        current_user = get_current_user()
        if not current_user:
            return jsonify({'error': 'User not authenticated'}), 401
            
        rant = Rant.query.filter_by(id=rant_id, user_id=current_user.id).first()
        if not rant:
            return jsonify({'error': 'Rant not found'}), 404
        
        data = request.get_json() or {}
        template_type = data.get('template_type', 'default')
        
        # Generate meme
        media_service = SimpleMediaService()
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
        current_user = get_current_user()
        if not current_user:
            return jsonify({'error': 'User not authenticated'}), 401
            
        rant = Rant.query.filter_by(id=rant_id, user_id=current_user.id).first()
        if not rant:
            return jsonify({'error': 'Rant not found'}), 404
        
        data = request.get_json() or {}
        duration = data.get('duration', 10)
        background_color = data.get('background_color', [30, 30, 30])
        
        # Generate video
        media_service = SimpleMediaService()
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
    """Transform rant content and generate text output using real AI"""
    try:
        current_user = get_current_user()
        if not current_user:
            return jsonify({'error': 'User not authenticated'}), 401
            
        rant = Rant.query.filter_by(id=rant_id, user_id=current_user.id).first()
        if not rant:
            return jsonify({'error': 'Rant not found'}), 404
        
        data = request.get_json() or {}
        transformation_type = data.get('transformation_type', 'poem')
        output_format = data.get('output_format', 'text')
        
        # Use real AI transformation with Gemini service
        try:
            # Create a new instance since app doesn't have gemini_service attribute
            from app.services.gemini_service import GeminiService
            gemini_service = GeminiService(current_app)
        except Exception as service_error:
            print(f"⚠️  Gemini service initialization error: {service_error}")
            return jsonify({"error": "AI service temporarily unavailable"}), 503
        
        print(f"🔍 Transform - Using Gemini for {transformation_type} transformation")
        print(f"🔍 Transform - Content preview: {rant.content[:50]}...")
        
        # Transform using real Gemini AI with fallback
        try:
            transformed_text = gemini_service.transform_content(rant.content, transformation_type)
            print(f"🔍 Transform - AI result preview: {transformed_text[:100]}...")
        except Exception as ai_error:
            print(f"⚠️  AI transformation failed: {ai_error}, using fallback")
            # Fallback to simple transformation if AI fails
            transformed_text = f"Enhanced {transformation_type} based on: {rant.content}\n\n[This content was generated using fallback mode due to AI service unavailability]"
        
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
