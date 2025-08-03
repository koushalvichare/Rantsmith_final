# Import all route blueprints
from .auth import auth_bp
from .rant_api import rant_bp
from .ai_processing import ai_bp
from .user_customization import user_bp

__all__ = ['auth_bp', 'rant_bp', 'ai_bp', 'user_bp']
