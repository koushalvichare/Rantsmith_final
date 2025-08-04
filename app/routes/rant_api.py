from flask_login import current_user
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
from app import db
from app.models import Rant, RantType, EmotionType
from app.services.rant_processor import RantProcessor
from app.utils.validators import validate_rant_data
from app.utils.auth import jwt_required

rant_bp = Blueprint('rant', __name__)

@rant_bp.route('/submit', methods=['POST'])
@jwt_required
def submit_rant():
    """Submit a new rant for processing"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or not data.get('content'):
            return jsonify({'error': 'Content is required'}), 400
        
        content = data.get('content')
        transformation_type = data.get('transformation_type', 'poem')
        tone = data.get('tone', 'neutral')
        privacy = data.get('privacy', 'private')
        input_type = data.get('input_type', 'text')
        
        # Create new rant
        rant = Rant(
            user_id=current_user.id,
            content=content,
            rant_type=RantType.TEXT if input_type == 'text' else RantType.AUDIO,
            input_type=input_type,
            processed=False,
            processing_status='pending'
        )
        
        db.session.add(rant)
        db.session.commit()
        
        return jsonify({
            'message': 'Rant submitted successfully',
            'rant_id': rant.id,
            'rant': {
                'id': rant.id,
                'content': rant.content,
                'input_type': rant.input_type,
                'created_at': rant.created_at.isoformat(),
                'processed': rant.processed
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error submitting rant: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@rant_bp.route('/history', methods=['GET'])
@jwt_required
def get_rant_history():
    """Get user's rant history"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        rants = Rant.query.filter_by(user_id=current_user.id)\
                          .order_by(Rant.created_at.desc())\
                          .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'rants': [rant.to_dict() for rant in rants.items],
            'total': rants.total,
            'page': page,
            'per_page': per_page,
            'has_next': rants.has_next,
            'has_prev': rants.has_prev
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@rant_bp.route('/<int:rant_id>', methods=['GET'])
@jwt_required
def get_rant(rant_id):
    """Get specific rant details"""
    try:
        rant = Rant.query.filter_by(id=rant_id, user_id=current_user.id).first()
        
        if not rant:
            return jsonify({'error': 'Rant not found'}), 404
        
        return jsonify(rant.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@rant_bp.route('/<int:rant_id>', methods=['DELETE'])
@jwt_required
def delete_rant(rant_id):
    """Delete a rant"""
    try:
        rant = Rant.query.filter_by(id=rant_id, user_id=current_user.id).first()
        
        if not rant:
            return jsonify({'error': 'Rant not found'}), 404
        
        # Delete associated file if exists
        if rant.file_path and os.path.exists(rant.file_path):
            os.remove(rant.file_path)
        
        db.session.delete(rant)
        db.session.commit()
        
        return jsonify({'message': 'Rant deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@rant_bp.route('/analytics', methods=['GET'])
@jwt_required
def get_rant_analytics():
    """Get user's rant analytics"""
    try:
        # Get emotion distribution
        emotion_counts = db.session.query(Rant.detected_emotion, db.func.count(Rant.id))\
                                  .filter_by(user_id=current_user.id)\
                                  .group_by(Rant.detected_emotion)\
                                  .all()
        
        # Get rant frequency over time
        monthly_counts = db.session.query(
            db.func.date_format(Rant.created_at, '%Y-%m'),
            db.func.count(Rant.id)
        ).filter_by(user_id=current_user.id)\
         .group_by(db.func.date_format(Rant.created_at, '%Y-%m'))\
         .order_by(db.func.date_format(Rant.created_at, '%Y-%m'))\
         .all()
        
        # Get average sentiment
        avg_sentiment = db.session.query(db.func.avg(Rant.sentiment_score))\
                                 .filter_by(user_id=current_user.id)\
                                 .scalar()
        
        return jsonify({
            'emotion_distribution': {
                emotion.value if emotion else 'unknown': count 
                for emotion, count in emotion_counts
            },
            'monthly_frequency': {
                month: count for month, count in monthly_counts
            },
            'average_sentiment': float(avg_sentiment) if avg_sentiment else 0.0,
            'total_rants': Rant.query.filter_by(user_id=current_user.id).count()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
