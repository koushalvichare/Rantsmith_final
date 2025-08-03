from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.services.simple_media_service import SimpleMediaService
from app.services.ai_service import AIService
from app.models import Rant, GeneratedContent, ContentType
from app import db
import logging

media_bp = Blueprint('media', __name__)

# Initialize services when needed
def get_media_service():
    return SimpleMediaService()

def get_ai_service():
    from flask import current_app
    ai_service = AIService()
    ai_service.openai_key = current_app.config.get('OPENAI_API_KEY')
    return ai_service

@media_bp.route('/upload-audio', methods=['POST'])
@login_required
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
@login_required
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

@media_bp.route('/generate-speech/<int:rant_id>', methods=['POST'])
@login_required
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
        media_service = get_media_service()
        result = media_service.text_to_speech(rant.content, language, slow)
        
        if result['success']:
            # Save generated content
            generated_content = GeneratedContent(
                user_id=current_user.id,
                rant_id=rant_id,
                content_type=ContentType.AUDIO,
                title=f"Speech from Rant {rant_id}",
                content=result['audio_data'],
                ai_model_used='gTTS'
            )
            db.session.add(generated_content)
            db.session.commit()
            
            return jsonify({
                'message': 'Speech generated successfully',
                'audio_data': result['audio_data'],
                'content_id': generated_content.id
            }), 200
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        logging.error(f"Speech generation error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@media_bp.route('/generate-meme/<int:rant_id>', methods=['POST'])
@login_required
def generate_meme(rant_id):
    """Generate meme from rant text"""
    try:
        rant = Rant.query.filter_by(id=rant_id, user_id=current_user.id).first()
        if not rant:
            return jsonify({'error': 'Rant not found'}), 404
        
        data = request.get_json() or {}
        template_type = data.get('template_type', 'default')
        
        # Generate meme
        result = media_service.generate_meme_image(rant.content, template_type)
        
        if result['success']:
            # Save generated content
            generated_content = GeneratedContent(
                user_id=current_user.id,
                rant_id=rant_id,
                content_type=ContentType.IMAGE,
                title=f"Meme from Rant {rant_id}",
                content=result['image_data'],
                ai_model_used='PIL'
            )
            db.session.add(generated_content)
            db.session.commit()
            
            return jsonify({
                'message': 'Meme generated successfully',
                'image_data': result['image_data'],
                'content_id': generated_content.id
            }), 200
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        logging.error(f"Meme generation error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@media_bp.route('/generate-video/<int:rant_id>', methods=['POST'])
@login_required
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
        result = media_service.create_video_from_text(rant.content, tuple(background_color), duration)
        
        if result['success']:
            # Save generated content
            generated_content = GeneratedContent(
                user_id=current_user.id,
                rant_id=rant_id,
                content_type=ContentType.VIDEO,
                title=f"Video from Rant {rant_id}",
                content=result['video_data'],
                ai_model_used='OpenCV'
            )
            db.session.add(generated_content)
            db.session.commit()
            
            return jsonify({
                'message': 'Video generated successfully',
                'video_data': result['video_data'],
                'content_id': generated_content.id
            }), 200
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        logging.error(f"Video generation error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@media_bp.route('/transform-with-ai/<int:rant_id>', methods=['POST'])
@login_required
def transform_with_ai(rant_id):
    """Transform rant content and generate multimedia output"""
    try:
        rant = Rant.query.filter_by(id=rant_id, user_id=current_user.id).first()
        if not rant:
            return jsonify({'error': 'Rant not found'}), 404
        
        data = request.get_json() or {}
        transformation_type = data.get('transformation_type', 'poem')
        output_format = data.get('output_format', 'text')  # text, audio, image, video
        
        # First, analyze and transform the rant content
        if not rant.processed:
            analysis = ai_service.analyze_rant(rant)
            rant.detected_emotion = analysis.get('emotion')
            rant.emotion_confidence = analysis.get('emotion_confidence')
            rant.sentiment_score = analysis.get('sentiment_score')
            rant.processed = True
            db.session.commit()
        
        # Transform the content based on type
        if transformation_type == 'poem':
            transformed_text = ai_service.transform_to_poem(rant.content)
        elif transformation_type == 'song':
            transformed_text = ai_service.transform_to_song(rant.content)
        elif transformation_type == 'story':
            transformed_text = ai_service.transform_to_story(rant.content)
        elif transformation_type == 'motivational':
            transformed_text = ai_service.transform_to_motivational(rant.content)
        else:
            transformed_text = rant.content
        
        # Generate output in requested format
        result = {'text': transformed_text}
        
        if output_format == 'audio':
            audio_result = media_service.text_to_speech(transformed_text)
            if audio_result['success']:
                result['audio_data'] = audio_result['audio_data']
        
        elif output_format == 'image':
            image_result = media_service.generate_meme_image(transformed_text)
            if image_result['success']:
                result['image_data'] = image_result['image_data']
        
        elif output_format == 'video':
            video_result = media_service.create_video_from_text(transformed_text)
            if video_result['success']:
                result['video_data'] = video_result['video_data']
        
        # Save the transformed content
        generated_content = GeneratedContent(
            user_id=current_user.id,
            rant_id=rant_id,
            content_type=ContentType.TEXT if output_format == 'text' else 
                        ContentType.AUDIO if output_format == 'audio' else
                        ContentType.IMAGE if output_format == 'image' else
                        ContentType.VIDEO,
            title=f"{transformation_type.title()} from Rant {rant_id}",
            content=result.get('text', ''),
            ai_model_used='Custom AI Service'
        )
        db.session.add(generated_content)
        db.session.commit()
        
        return jsonify({
            'message': 'Content transformed successfully',
            'transformation_type': transformation_type,
            'output_format': output_format,
            'content_id': generated_content.id,
            **result
        }), 200
        
    except Exception as e:
        logging.error(f"AI transformation error: {e}")
        return jsonify({'error': 'Internal server error'}), 500
