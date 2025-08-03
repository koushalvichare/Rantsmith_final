from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import GeneratedContent, SuggestedAction

user_bp = Blueprint('user', __name__)

@user_bp.route('/preferences', methods=['GET'])
@login_required
def get_preferences():
    """Get user preferences"""
    return jsonify({
        'preferred_output_format': current_user.preferred_output_format,
        'ai_personality': current_user.ai_personality,
        'display_name': current_user.display_name,
        'bio': current_user.bio,
        'avatar_url': current_user.avatar_url
    }), 200

@user_bp.route('/preferences', methods=['PUT'])
@login_required
def update_preferences():
    """Update user preferences"""
    try:
        data = request.get_json()
        
        # Update preferences
        if 'preferred_output_format' in data:
            allowed_formats = ['text', 'audio', 'video', 'meme']
            if data['preferred_output_format'] in allowed_formats:
                current_user.preferred_output_format = data['preferred_output_format']
        
        if 'ai_personality' in data:
            allowed_personalities = ['supportive', 'sarcastic', 'humorous', 'motivational']
            if data['ai_personality'] in allowed_personalities:
                current_user.ai_personality = data['ai_personality']
        
        if 'display_name' in data:
            current_user.display_name = data['display_name']
        
        if 'bio' in data:
            current_user.bio = data['bio']
        
        if 'avatar_url' in data:
            current_user.avatar_url = data['avatar_url']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Preferences updated successfully',
            'preferences': {
                'preferred_output_format': current_user.preferred_output_format,
                'ai_personality': current_user.ai_personality,
                'display_name': current_user.display_name,
                'bio': current_user.bio,
                'avatar_url': current_user.avatar_url
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/favorites', methods=['GET'])
@login_required
def get_favorites():
    """Get user's favorite content"""
    try:
        favorites = GeneratedContent.query.filter_by(
            user_id=current_user.id,
            is_favorite=True
        ).order_by(GeneratedContent.created_at.desc()).all()
        
        return jsonify({
            'favorites': [content.to_dict() for content in favorites]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/favorites/<int:content_id>', methods=['POST'])
@login_required
def add_to_favorites(content_id):
    """Add content to favorites"""
    try:
        content = GeneratedContent.query.filter_by(
            id=content_id,
            user_id=current_user.id
        ).first()
        
        if not content:
            return jsonify({'error': 'Content not found'}), 404
        
        content.is_favorite = True
        db.session.commit()
        
        return jsonify({'message': 'Added to favorites'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/favorites/<int:content_id>', methods=['DELETE'])
@login_required
def remove_from_favorites(content_id):
    """Remove content from favorites"""
    try:
        content = GeneratedContent.query.filter_by(
            id=content_id,
            user_id=current_user.id
        ).first()
        
        if not content:
            return jsonify({'error': 'Content not found'}), 404
        
        content.is_favorite = False
        db.session.commit()
        
        return jsonify({'message': 'Removed from favorites'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/rate-content/<int:content_id>', methods=['POST'])
@login_required
def rate_content(content_id):
    """Rate generated content"""
    try:
        data = request.get_json()
        rating = data.get('rating')
        
        if not rating or rating not in [1, 2, 3, 4, 5]:
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        
        content = GeneratedContent.query.filter_by(
            id=content_id,
            user_id=current_user.id
        ).first()
        
        if not content:
            return jsonify({'error': 'Content not found'}), 404
        
        content.user_rating = rating
        db.session.commit()
        
        return jsonify({'message': 'Content rated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/dashboard', methods=['GET'])
@login_required
def get_dashboard_data():
    """Get dashboard data for user"""
    try:
        # Get recent rants
        recent_rants = db.session.query(
            db.func.count(db.text('id'))
        ).filter(
            db.text('user_id = :user_id'),
            db.text('created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)')
        ).params(user_id=current_user.id).scalar()
        
        # Get content generated
        content_generated = GeneratedContent.query.filter_by(
            user_id=current_user.id
        ).count()
        
        # Get favorite content count
        favorites_count = GeneratedContent.query.filter_by(
            user_id=current_user.id,
            is_favorite=True
        ).count()
        
        # Get recent generated content
        recent_content = GeneratedContent.query.filter_by(
            user_id=current_user.id
        ).order_by(GeneratedContent.created_at.desc()).limit(5).all()
        
        return jsonify({
            'stats': {
                'recent_rants': recent_rants or 0,
                'content_generated': content_generated,
                'favorites_count': favorites_count
            },
            'recent_content': [content.to_dict() for content in recent_content],
            'user': current_user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
