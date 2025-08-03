from flask import Blueprint, request, jsonify
from app import db
from app.models import Rant, GeneratedContent, ContentType, EmotionType
from app.services.ai_service import AIService
from app.services.content_generator import ContentGenerator
from app.utils.auth import jwt_required

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/process/<int:rant_id>', methods=['POST'])
@jwt_required
def process_rant(rant_id):
    """Process a rant with AI"""
    try:
        rant = Rant.query.filter_by(id=rant_id, user_id=request.current_user.id).first()
        
        if not rant:
            return jsonify({'error': 'Rant not found'}), 404
        
        if rant.processed:
            return jsonify({'error': 'Rant already processed'}), 400
        
        # Initialize AI service
        ai_service = AIService()
        
        # Analyze rant
        analysis = ai_service.analyze_rant(rant)
        
        # Update rant with analysis - convert emotion string to enum
        emotion_str = analysis.get('emotion', 'neutral')
        if isinstance(emotion_str, str):
            try:
                # Try to find matching EmotionType
                rant.detected_emotion = next(
                    (emotion for emotion in EmotionType if emotion.value.lower() == emotion_str.lower()),
                    EmotionType.NEUTRAL
                )
            except:
                rant.detected_emotion = EmotionType.NEUTRAL
        else:
            rant.detected_emotion = emotion_str
            
        rant.emotion_confidence = analysis.get('emotion_confidence')
        rant.sentiment_score = analysis.get('sentiment_score')
        rant.keywords = analysis.get('keywords')
        rant.processing_status = 'completed'
        rant.processed = True
        
        db.session.commit()
        
        return jsonify({
            'message': 'Rant processed successfully',
            'analysis': analysis,
            'rant': rant.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/generate-content/<int:rant_id>', methods=['POST'])
@jwt_required
def generate_content(rant_id):
    """Generate content from a rant"""
    try:
        data = request.get_json()
        content_type = data.get('content_type', 'text')
        
        rant = Rant.query.filter_by(id=rant_id, user_id=request.current_user.id).first()
        
        if not rant:
            return jsonify({'error': 'Rant not found'}), 404
        
        # Initialize content generator
        content_generator = ContentGenerator()
        
        # Generate content based on type
        if content_type == 'meme':
            result = content_generator.generate_meme(rant)
        elif content_type == 'tweet':
            result = content_generator.generate_tweet(rant)
        elif content_type == 'song':
            result = content_generator.generate_song(rant)
        elif content_type == 'script':
            result = content_generator.generate_script(rant)
        elif content_type == 'audio':
            result = content_generator.generate_audio(rant)
        elif content_type == 'video':
            result = content_generator.generate_video(rant)
        else:
            result = content_generator.generate_text(rant)
        
        # Save generated content
        generated_content = GeneratedContent(
            user_id=request.current_user.id,
            rant_id=rant_id,
            content_type=ContentType(content_type),
            title=result.get('title'),
            content=result.get('content'),
            file_path=result.get('file_path'),
            ai_model_used=result.get('model_used'),
            processing_time=result.get('processing_time'),
            quality_score=result.get('quality_score')
        )
        
        db.session.add(generated_content)
        db.session.commit()
        
        return jsonify({
            'message': 'Content generated successfully',
            'content': generated_content.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/suggest-actions/<int:rant_id>', methods=['POST'])
@jwt_required
def suggest_actions(rant_id):
    """Generate action suggestions for a rant"""
    try:
        rant = Rant.query.filter_by(id=rant_id, user_id=request.current_user.id).first()
        
        if not rant:
            return jsonify({'error': 'Rant not found'}), 404
        
        # Initialize AI service
        ai_service = AIService()
        
        # Generate action suggestions
        suggestions = ai_service.suggest_actions(rant)
        
        return jsonify({
            'message': 'Action suggestions generated',
            'suggestions': suggestions
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/customize-personality', methods=['POST'])
@jwt_required
def customize_personality():
    """Customize AI personality for user"""
    try:
        data = request.get_json()
        
        allowed_personalities = ['supportive', 'sarcastic', 'humorous', 'motivational', 'professional']
        personality = data.get('personality', 'supportive')
        
        if personality not in allowed_personalities:
            return jsonify({'error': 'Invalid personality type'}), 400
        
        request.current_user.ai_personality = personality
        db.session.commit()
        
        return jsonify({
            'message': 'AI personality updated successfully',
            'personality': personality
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/content-history', methods=['GET'])
@jwt_required
def get_content_history():
    """Get user's generated content history"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        content_type = request.args.get('type')
        
        query = GeneratedContent.query.filter_by(user_id=request.current_user.id)
        
        if content_type:
            query = query.filter_by(content_type=ContentType(content_type))
        
        contents = query.order_by(GeneratedContent.created_at.desc())\
                       .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'contents': [content.to_dict() for content in contents.items],
            'total': contents.total,
            'page': page,
            'per_page': per_page,
            'has_next': contents.has_next,
            'has_prev': contents.has_prev
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Additional routes for frontend compatibility
@ai_bp.route('/analyze/<int:rant_id>', methods=['POST'])
@jwt_required
def analyze_rant_endpoint(rant_id):
    """Analyze a rant with AI - frontend compatible endpoint"""
    return process_rant(rant_id)

@ai_bp.route('/generate/text/<int:rant_id>', methods=['POST'])
@jwt_required
def generate_text_endpoint(rant_id):
    """Generate text content from a rant"""
    try:
        rant = Rant.query.filter_by(id=rant_id, user_id=request.current_user.id).first()
        
        if not rant:
            return jsonify({'error': 'Rant not found'}), 404
        
        # Generate text content
        content_generator = ContentGenerator()
        result = content_generator.generate_text(rant)
        
        # Save generated content
        generated_content = GeneratedContent(
            rant_id=rant_id,
            user_id=request.current_user.id,
            content_type=ContentType.TEXT,
            content=result['content'],
            ai_model_used=result.get('model_used', 'gemini-1.5-flash')
        )
        
        db.session.add(generated_content)
        db.session.commit()
        
        return jsonify({
            'message': 'Text generated successfully',
            'generated_text': result['content'],
            'model_used': result.get('model_used', 'gemini-1.5-flash')
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/generate/meme/<int:rant_id>', methods=['POST'])
@jwt_required
def generate_meme_endpoint(rant_id):
    """Generate meme content from a rant"""
    try:
        rant = Rant.query.filter_by(id=rant_id, user_id=request.current_user.id).first()
        
        if not rant:
            return jsonify({'error': 'Rant not found'}), 404
        
        # Generate meme content
        content_generator = ContentGenerator()
        result = content_generator.generate_meme(rant)
        
        # Save generated content
        generated_content = GeneratedContent(
            rant_id=rant_id,
            user_id=request.current_user.id,
            content_type=ContentType.MEME,
            content=result['content'],
            ai_model_used=result.get('model_used', 'gemini-1.5-flash')
        )
        
        db.session.add(generated_content)
        db.session.commit()
        
        return jsonify({
            'message': 'Meme generated successfully',
            'meme_text': result['content'],
            'model_used': result.get('model_used', 'gemini-1.5-flash')
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/generate/tweet/<int:rant_id>', methods=['POST'])
@jwt_required
def generate_tweet_endpoint(rant_id):
    """Generate tweet content from a rant"""
    try:
        rant = Rant.query.filter_by(id=rant_id, user_id=request.current_user.id).first()
        
        if not rant:
            return jsonify({'error': 'Rant not found'}), 404
        
        # Generate tweet content
        content_generator = ContentGenerator()
        result = content_generator.generate_tweet(rant)
        
        # Save generated content
        generated_content = GeneratedContent(
            rant_id=rant_id,
            user_id=request.current_user.id,
            content_type=ContentType.TWEET,
            content=result['content'],
            ai_model_used=result.get('model_used', 'gemini-1.5-flash')
        )
        
        db.session.add(generated_content)
        db.session.commit()
        
        return jsonify({
            'message': 'Tweet generated successfully',
            'tweet_text': result['content'],
            'model_used': result.get('model_used', 'gemini-1.5-flash')
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
