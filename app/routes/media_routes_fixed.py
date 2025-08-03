from flask import Blueprint, request, jsonify
from app.services.simple_media_service import SimpleMediaService
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
            
            # Get user from database
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 401
            
            # Store user in request context
            request.current_user = user
            return f(*args, **kwargs)
        except Exception as e:
            logging.error(f"JWT verification error: {e}")
            return jsonify({'error': 'Authentication failed'}), 401
    return decorated_function

media_bp = Blueprint('media', __name__)

# Initialize services when needed
def get_media_service():
    return SimpleMediaService()

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
        media_service = get_media_service()
        result = media_service.process_audio_file(audio_file)
        
        if result['success']:
            # Create a new rant from the transcribed text
            rant = Rant(
                user_id=request.current_user.id,
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
        media_service = get_media_service()
        result = media_service.process_image_file(image_file)
        
        if result['success']:
            # For now, we'll just return the image data
            # In the future, we could use OCR to extract text from images
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

@media_bp.route('/transform-with-ai/<int:rant_id>', methods=['POST'])
@jwt_required
def transform_with_ai(rant_id):
    """Transform rant content using AI"""
    try:
        rant = Rant.query.filter_by(id=rant_id, user_id=request.current_user.id).first()
        
        if not rant:
            return jsonify({'error': 'Rant not found'}), 404
        
        data = request.get_json() or {}
        transformation_type = data.get('transformation_type', 'poem')
        output_format = data.get('output_format', 'text')
        
        # Get AI service
        from app.services.ai_service import AIService
        ai_service = AIService()
        
        # Transform content based on type
        if transformation_type == 'poem':
            result = ai_service.transform_to_poem(rant.content)
        elif transformation_type == 'rap':
            result = ai_service.transform_to_rap(rant.content)
        elif transformation_type == 'song':
            result = ai_service.transform_to_song(rant.content)
        elif transformation_type == 'story':
            result = ai_service.transform_to_story(rant.content)
        elif transformation_type == 'motivational':
            result = ai_service.transform_to_motivational(rant.content)
        elif transformation_type == 'comedy':
            result = ai_service.transform_to_comedy(rant.content)
        else:
            # Default transformation
            result = ai_service.transform_to_poem(rant.content)
        
        if result and 'text' in result:
            # Save generated content
            generated_content = GeneratedContent(
                user_id=request.current_user.id,
                rant_id=rant_id,
                content_type=ContentType.TEXT,
                title=f"{transformation_type.title()} from Rant {rant_id}",
                content=result['text'],
                ai_model_used=result.get('model_used', 'gemini-pro')
            )
            db.session.add(generated_content)
            db.session.commit()
            
            return jsonify({
                'message': f'Content transformed to {transformation_type} successfully',
                'text': result['text'],
                'content_id': generated_content.id,
                'model_used': result.get('model_used', 'gemini-pro')
            }), 200
        else:
            return jsonify({'error': 'AI transformation failed'}), 400
            
    except Exception as e:
        logging.error(f"AI transformation error: {e}")
        return jsonify({'error': f'AI transformation failed: {str(e)}'}), 500

# Health check endpoint
@media_bp.route('/health', methods=['GET'])
def health_check():
    """Health check for media service"""
    return jsonify({
        'status': 'healthy',
        'message': 'Media service is running',
        'endpoints': [
            '/upload-audio',
            '/upload-image', 
            '/transform-with-ai/<rant_id>'
        ]
    }), 200
