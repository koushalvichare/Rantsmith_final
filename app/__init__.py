from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from config import config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    CORS(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Add a simple home route for testing
    @app.route('/')
    def home():
        return {
            'message': 'Welcome to RantSmith AI!',
            'status': 'running',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/auth/*',
                'rants': '/api/rant/*',
                'ai': '/api/ai/*',
                'user': '/api/user/*',
                'health': '/health'
            }
        }
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'RantSmith AI is running'}
    
    # Register blueprints
    try:
        from app.routes.auth import auth_bp
        from app.routes.rant_api import rant_bp
        from app.routes.ai_processing import ai_bp
        from app.routes.user_customization import user_bp
        from app.routes.media_routes import media_bp
        
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(rant_bp, url_prefix='/api/rant')
        app.register_blueprint(ai_bp, url_prefix='/api/ai')
        app.register_blueprint(user_bp, url_prefix='/api/user')
        app.register_blueprint(media_bp, url_prefix='/api/media')
        
        print("All blueprints registered successfully!")
        
    except ImportError as e:
        print(f"Error importing blueprints: {e}")
        print("Running with basic routes only")
    
    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully!")
        except Exception as e:
            print(f"Error creating database tables: {e}")
    
    return app
