from app import create_app, db
from app.models import User, Rant, GeneratedContent, SuggestedAction
import os

def create_database():
    """Create database tables"""
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

def create_sample_data():
    """Create sample data for testing"""
    app = create_app()
    with app.app_context():
        # Create sample user
        user = User(
            username='testuser',
            email='test@example.com',
            display_name='Test User',
            bio='A test user for RantSmith AI',
            preferred_output_format='text',
            ai_personality='supportive'
        )
        user.set_password('TestPassword123')
        
        db.session.add(user)
        db.session.commit()
        
        print("Sample data created successfully!")

if __name__ == '__main__':
    create_database()
    create_sample_data()
