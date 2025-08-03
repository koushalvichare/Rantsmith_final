from datetime import datetime
from enum import Enum
from app import db

class RantType(Enum):
    """Types of rants"""
    TEXT = "text"
    AUDIO = "audio"
    VIDEO = "video"

class EmotionType(Enum):
    """Detected emotions"""
    ANGRY = "angry"
    FRUSTRATED = "frustrated"
    SAD = "sad"
    ANXIOUS = "anxious"
    EXCITED = "excited"
    HAPPY = "happy"
    CONFUSED = "confused"
    NEUTRAL = "neutral"

class Rant(db.Model):
    """Rant model for storing user rants"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Content
    content = db.Column(db.Text, nullable=False)
    rant_type = db.Column(db.Enum(RantType), default=RantType.TEXT)
    input_type = db.Column(db.String(50), default='text')  # text, audio, image, video
    file_path = db.Column(db.String(255))  # For audio/video files
    
    # AI Analysis
    detected_emotion = db.Column(db.Enum(EmotionType))
    emotion_confidence = db.Column(db.Float)
    keywords = db.Column(db.Text)  # JSON string of extracted keywords
    sentiment_score = db.Column(db.Float)  # -1 to 1 scale
    
    # Metadata
    processed = db.Column(db.Boolean, default=False)
    processing_status = db.Column(db.String(50), default='pending')  # pending, processing, completed, failed
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    
    # Relationships
    generated_content = db.relationship('GeneratedContent', backref='rant', lazy=True)
    
    def to_dict(self):
        """Convert rant to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content': self.content,
            'rant_type': self.rant_type.value if self.rant_type else None,
            'file_path': self.file_path,
            'detected_emotion': self.detected_emotion.value if self.detected_emotion else None,
            'emotion_confidence': self.emotion_confidence,
            'keywords': self.keywords,
            'sentiment_score': self.sentiment_score,
            'processed': self.processed,
            'processing_status': self.processing_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None
        }
    
    def __repr__(self):
        return f'<Rant {self.id} by User {self.user_id}>'
