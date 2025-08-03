from datetime import datetime
from app.models import Rant, EmotionType
from app.services.ai_service import AIService
from app import db
import json

class RantProcessor:
    """Service for processing rants through the AI pipeline"""
    
    def __init__(self):
        self.ai_service = AIService()
    
    def process_rant(self, rant: Rant) -> dict:
        """Process a rant through the complete AI pipeline"""
        try:
            # Update status
            rant.processing_status = 'processing'
            db.session.commit()
            
            # Analyze the rant
            analysis = self.ai_service.analyze_rant(rant)
            
            # Update rant with analysis results
            rant.detected_emotion = analysis.get('emotion')
            rant.emotion_confidence = analysis.get('emotion_confidence', 0.0)
            rant.sentiment_score = analysis.get('sentiment_score', 0.0)
            rant.keywords = analysis.get('keywords', '[]')
            rant.processed = True
            rant.processing_status = 'completed'
            rant.processed_at = datetime.utcnow()
            
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Rant processed successfully',
                'analysis': analysis,
                'rant_id': rant.id
            }
            
        except Exception as e:
            # Update status on error
            rant.processing_status = 'failed'
            db.session.commit()
            
            return {
                'success': False,
                'message': f'Processing failed: {str(e)}',
                'rant_id': rant.id
            }
    
    def extract_audio_text(self, file_path: str) -> str:
        """Extract text from audio file using speech-to-text"""
        # This would integrate with services like:
        # - Google Speech-to-Text
        # - AWS Transcribe
        # - OpenAI Whisper
        # For now, return placeholder
        return "Audio transcription not implemented yet"
    
    def extract_video_text(self, file_path: str) -> str:
        """Extract text from video file"""
        # This would:
        # 1. Extract audio from video
        # 2. Use speech-to-text on audio
        # 3. Optionally use OCR on video frames
        return "Video transcription not implemented yet"
    
    def validate_rant_content(self, content: str) -> dict:
        """Validate rant content before processing"""
        if not content or len(content.strip()) < 10:
            return {
                'valid': False,
                'message': 'Rant must be at least 10 characters long'
            }
        
        if len(content) > 5000:
            return {
                'valid': False,
                'message': 'Rant is too long (max 5000 characters)'
            }
        
        # Check for inappropriate content (basic filter)
        inappropriate_words = ['spam', 'advertisement']  # Extend as needed
        if any(word in content.lower() for word in inappropriate_words):
            return {
                'valid': False,
                'message': 'Content contains inappropriate material'
            }
        
        return {
            'valid': True,
            'message': 'Content is valid'
        }
    
    def get_processing_statistics(self, user_id: int) -> dict:
        """Get processing statistics for a user"""
        try:
            total_rants = Rant.query.filter_by(user_id=user_id).count()
            processed_rants = Rant.query.filter_by(user_id=user_id, processed=True).count()
            pending_rants = Rant.query.filter_by(user_id=user_id, processing_status='pending').count()
            failed_rants = Rant.query.filter_by(user_id=user_id, processing_status='failed').count()
            
            # Get emotion distribution
            emotion_counts = {}
            for emotion in EmotionType:
                count = Rant.query.filter_by(user_id=user_id, detected_emotion=emotion).count()
                emotion_counts[emotion.value] = count
            
            # Get average sentiment
            avg_sentiment = db.session.query(db.func.avg(Rant.sentiment_score))\
                                   .filter_by(user_id=user_id)\
                                   .scalar()
            
            return {
                'total_rants': total_rants,
                'processed_rants': processed_rants,
                'pending_rants': pending_rants,
                'failed_rants': failed_rants,
                'processing_rate': processed_rants / total_rants if total_rants > 0 else 0,
                'emotion_distribution': emotion_counts,
                'average_sentiment': float(avg_sentiment) if avg_sentiment else 0.0
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'total_rants': 0,
                'processed_rants': 0,
                'pending_rants': 0,
                'failed_rants': 0,
                'processing_rate': 0.0,
                'emotion_distribution': {},
                'average_sentiment': 0.0
            }
