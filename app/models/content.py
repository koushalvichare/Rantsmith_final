from datetime import datetime
from enum import Enum
from app import db

class ContentType(Enum):
    """Types of generated content"""
    TEXT = "text"
    MEME = "meme"
    TWEET = "tweet"
    SONG = "song"
    SCRIPT = "script"
    AUDIO = "audio"
    VIDEO = "video"

class ActionType(Enum):
    """Types of suggested actions"""
    SHARE_SOCIAL = "share_social"
    SAVE_LOCAL = "save_local"
    SEND_MESSAGE = "send_message"
    SCHEDULE_POST = "schedule_post"
    CREATE_REMINDER = "create_reminder"
    BOOK_THERAPY = "book_therapy"
    CALL_FRIEND = "call_friend"
    EXERCISE = "exercise"
    MEDITATE = "meditate"

class GeneratedContent(db.Model):
    """Generated content from AI processing"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rant_id = db.Column(db.Integer, db.ForeignKey('rant.id'), nullable=False)
    
    # Content details
    content_type = db.Column(db.Enum(ContentType), nullable=False)
    title = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(255))  # For generated media files
    
    # Metadata
    ai_model_used = db.Column(db.String(100))
    processing_time = db.Column(db.Float)  # Time taken to generate
    quality_score = db.Column(db.Float)  # AI-assessed quality (0-1)
    
    # User interaction
    user_rating = db.Column(db.Integer)  # 1-5 stars
    is_favorite = db.Column(db.Boolean, default=False)
    shared_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    suggested_actions = db.relationship('SuggestedAction', backref='content', lazy=True)
    
    def to_dict(self):
        """Convert content to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'rant_id': self.rant_id,
            'content_type': self.content_type.value if self.content_type else None,
            'title': self.title,
            'content': self.content,
            'file_path': self.file_path,
            'ai_model_used': self.ai_model_used,
            'processing_time': self.processing_time,
            'quality_score': self.quality_score,
            'user_rating': self.user_rating,
            'is_favorite': self.is_favorite,
            'shared_count': self.shared_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<GeneratedContent {self.id} - {self.content_type.value}>'

class SuggestedAction(db.Model):
    """AI-suggested actions based on rant analysis"""
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('generated_content.id'), nullable=False)
    
    # Action details
    action_type = db.Column(db.Enum(ActionType), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    action_data = db.Column(db.Text)  # JSON string with action-specific data
    
    # Priority and relevance
    priority = db.Column(db.Integer, default=1)  # 1-5, 5 being highest
    relevance_score = db.Column(db.Float)  # 0-1 based on AI analysis
    
    # User interaction
    was_executed = db.Column(db.Boolean, default=False)
    user_feedback = db.Column(db.String(20))  # helpful, not_helpful, irrelevant
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    executed_at = db.Column(db.DateTime)
    
    def to_dict(self):
        """Convert action to dictionary"""
        return {
            'id': self.id,
            'content_id': self.content_id,
            'action_type': self.action_type.value if self.action_type else None,
            'title': self.title,
            'description': self.description,
            'action_data': self.action_data,
            'priority': self.priority,
            'relevance_score': self.relevance_score,
            'was_executed': self.was_executed,
            'user_feedback': self.user_feedback,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'executed_at': self.executed_at.isoformat() if self.executed_at else None
        }
    
    def __repr__(self):
        return f'<SuggestedAction {self.id} - {self.action_type.value}>'
