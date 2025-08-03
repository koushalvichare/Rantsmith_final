from datetime import datetime
try:
    from flask_sqlalchemy import SQLAlchemy
    from flask_login import UserMixin
    from werkzeug.security import generate_password_hash, check_password_hash
    from app import db
    
    class User(UserMixin, db.Model):
        """User model for authentication and profile management"""
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password_hash = db.Column(db.String(255), nullable=False)
        
        # Profile information
        display_name = db.Column(db.String(100))
        bio = db.Column(db.Text)
        avatar_url = db.Column(db.String(255))
        
        # Preferences
        preferred_output_format = db.Column(db.String(50), default='text')  # text, audio, video, meme
        ai_personality = db.Column(db.String(50), default='supportive')  # supportive, sarcastic, humorous, motivational
        
        # Timestamps
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        last_login = db.Column(db.DateTime)
        
        # Relationships
        rants = db.relationship('Rant', backref='user', lazy=True)
        content_history = db.relationship('GeneratedContent', backref='user', lazy=True)
        
        def set_password(self, password):
            """Set password hash"""
            self.password_hash = generate_password_hash(password)
        
        def check_password(self, password):
            """Check password against hash"""
            return check_password_hash(self.password_hash, password)
        
        def to_dict(self):
            """Convert user to dictionary"""
            return {
                'id': self.id,
                'username': self.username,
                'email': self.email,
                'display_name': self.display_name,
                'bio': self.bio,
                'avatar_url': self.avatar_url,
                'preferred_output_format': self.preferred_output_format,
                'ai_personality': self.ai_personality,
                'created_at': self.created_at.isoformat() if self.created_at else None,
                'last_login': self.last_login.isoformat() if self.last_login else None
            }
        
        def __repr__(self):
            return f'<User {self.username}>'

except ImportError as e:
    print(f"Warning: Could not import dependencies for User model: {e}")
    # Create a dummy class for testing
    class User:
        def __init__(self):
            pass
