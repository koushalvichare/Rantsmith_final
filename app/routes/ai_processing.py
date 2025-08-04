from flask_login import current_user
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from app import db
from app.models import Rant, GeneratedContent, ContentType, EmotionType
from app.services.gemini_service import GeminiService
from app.utils.auth import jwt_required
import json

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/process/<int:rant_id>', methods=['POST'])
@jwt_required
def process_rant(rant_id):
    """Process a rant with AI using Gemini Service"""
    try:
        rant = Rant.query.filter_by(id=rant_id, user_id=current_user.id).first()
        
        if not rant:
            return jsonify({'error': 'Rant not found'}), 404
        
        if rant.processed:
            return jsonify({'error': 'Rant already processed'}), 400
        
        # Initialize Gemini service
        gemini_service = current_app.gemini_service
        
        # Analyze rant
        analysis = gemini_service.analyze_rant(rant)
        
        # Update rant with analysis
        emotion_str = analysis.get('emotion', 'neutral')
        try:
            rant.detected_emotion = EmotionType(emotion_str.lower())
        except ValueError:
            rant.detected_emotion = EmotionType.NEUTRAL
            
        rant.emotion_confidence = analysis.get('emotion_confidence')
        rant.sentiment_score = analysis.get('sentiment_score')
        # Ensure keywords are stored as a JSON string
        rant.keywords = json.dumps(analysis.get('keywords', []))
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
    """Generate content from a rant using Gemini Service"""
    try:
        data = request.get_json()
        content_type = data.get('content_type', 'text')
        
        rant = Rant.query.filter_by(id=rant_id, user_id=current_user.id).first()
        
        if not rant:
            return jsonify({'error': 'Rant not found'}), 404
        
        # Initialize Gemini service
        gemini_service = current_app.gemini_service
        
        # Generate content based on type
        transformation_map = {
            'poem': 'poem',
            'song': 'song',
            'story': 'story',
            'motivational': 'motivational',
            'letter': 'letter'
        }
        
        transformation_type = transformation_map.get(content_type)
        if not transformation_type:
            return jsonify({'error': 'Invalid content type'}), 400

        result = gemini_service.transform_content(rant.content, transformation_type)
        
        # Save generated content
        generated_content = GeneratedContent(
            user_id=current_user.id,
            rant_id=rant_id,
            content_type=ContentType(content_type),
            title=f"{transformation_type.capitalize()} from Rant #{rant.id}",
            content=result,
            ai_model_used='gemini-1.5-pro-latest'
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
        rant = Rant.query.filter_by(id=rant_id, user_id=current_user.id).first()
        
        if not rant:
            return jsonify({'error': 'Rant not found'}), 404
        
        # This can be expanded with Gemini in the future, for now, it's a placeholder
        # from app.services.ai_service import AIService
        # ai_service = AIService()
        # suggestions = ai_service.suggest_actions(rant)
        
        # Placeholder suggestions
        suggestions = [
            {'type': 'journal', 'title': 'Write it down', 'description': 'Journaling can help clarify your thoughts.'},
            {'type': 'talk', 'title': 'Talk to someone', 'description': 'Sharing with a friend can lighten the load.'}
        ]
        
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
        
        current_user.ai_personality = personality
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
        
        query = GeneratedContent.query.filter_by(user_id=current_user.id)
        
        if content_type:
            query = query.filter_by(content_type=ContentType(content_type))
        
        contents = query.order_by(GeneratedContent.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
        
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

@ai_bp.route('/chat', methods=['POST'])
@jwt_required
def chat_with_ai():
    """Chat with AI using Gemini"""
    try:
        data = request.get_json()
        
        if not data or not data.get('message'):
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data.get('message')
        personality = data.get('personality', 'supportive')
        conversation_id = data.get('conversation_id')
        
        # Use the global Gemini service that's already initialized
        gemini_service = current_app.gemini_service
        
        # Debug information
        print(f"🔍 Chat - API key present: {bool(gemini_service.gemini_key)}")
        print(f"🔍 Chat - Model available: {bool(gemini_service.model)}")
        print(f"🔍 Chat - User message: {user_message[:50]}...")
        
        # Create a temporary rant object for the AI response
        from app.models import Rant
        temp_rant = Rant(
            content=user_message,
            user_id=current_user.id
        )
        
        # Generate AI response using Gemini
        ai_response = gemini_service.generate_response(temp_rant, personality)
        print(f"🔍 Chat - AI response generated: {ai_response[:50]}...")
        
        return jsonify({
            'response': ai_response,
            'personality': personality,
            'timestamp': datetime.utcnow().isoformat(),
            'conversation_id': conversation_id
        }), 200
        
    except Exception as e:
        print(f"❌ Chat error: {str(e)}")
        return jsonify({'error': f'AI chat failed: {str(e)}'}), 500

@ai_bp.route('/test-gemini', methods=['GET'])
@jwt_required
def test_gemini():
    """Test Gemini API configuration"""
    try:
        # Use the global Gemini service
        gemini_service = current_app.gemini_service
        
        # Check configuration
        api_key_present = bool(gemini_service.gemini_key)
        model_available = bool(gemini_service.model)
        
        # Try a simple test if model is available
        test_response = None
        if gemini_service.model:
            try:
                test_content = "Hello, this is a test."
                response = gemini_service.model.generate_content(test_content)
                test_response = response.text[:100] + "..." if len(response.text) > 100 else response.text
            except Exception as e:
                test_response = f"Model test failed: {str(e)}"
        
        return jsonify({
            'api_key_present': api_key_present,
            'api_key_value': gemini_service.gemini_key[:10] + "..." if gemini_service.gemini_key else None,
            'model_available': model_available,
            'model_name': 'gemini-1.5-pro-latest' if model_available else None,
            'test_response': test_response,
            'config_debug': {
                'GEMINI_API_KEY': current_app.config.get('GEMINI_API_KEY', 'Not set')[:10] + "..." if current_app.config.get('GEMINI_API_KEY') else 'Not set'
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Gemini test failed: {str(e)}'}), 500
