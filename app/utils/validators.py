import re
from typing import Dict, Any

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username: str) -> Dict[str, Any]:
    """Validate username"""
    if not username:
        return {'valid': False, 'message': 'Username is required'}
    
    if len(username) < 3:
        return {'valid': False, 'message': 'Username must be at least 3 characters'}
    
    if len(username) > 20:
        return {'valid': False, 'message': 'Username must be less than 20 characters'}
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return {'valid': False, 'message': 'Username can only contain letters, numbers, and underscores'}
    
    return {'valid': True, 'message': 'Username is valid'}

def validate_password(password: str) -> Dict[str, Any]:
    """Validate password strength"""
    if not password:
        return {'valid': False, 'message': 'Password is required'}
    
    if len(password) < 8:
        return {'valid': False, 'message': 'Password must be at least 8 characters'}
    
    if not re.search(r'[A-Z]', password):
        return {'valid': False, 'message': 'Password must contain at least one uppercase letter'}
    
    if not re.search(r'[a-z]', password):
        return {'valid': False, 'message': 'Password must contain at least one lowercase letter'}
    
    if not re.search(r'\d', password):
        return {'valid': False, 'message': 'Password must contain at least one number'}
    
    return {'valid': True, 'message': 'Password is valid'}

def validate_rant_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate rant submission data"""
    if not data:
        return {'valid': False, 'message': 'No data provided'}
    
    content = data.get('content', '')
    
    if not content and not data.get('file'):
        return {'valid': False, 'message': 'Content or file is required'}
    
    if content and len(content.strip()) < 5:
        return {'valid': False, 'message': 'Content must be at least 5 characters'}
    
    if content and len(content) > 5000:
        return {'valid': False, 'message': 'Content is too long (max 5000 characters)'}
    
    return {'valid': True, 'message': 'Rant data is valid'}

def validate_content_type(content_type: str) -> bool:
    """Validate content generation type"""
    valid_types = ['text', 'meme', 'tweet', 'song', 'script', 'audio', 'video']
    return content_type in valid_types

def validate_personality_type(personality: str) -> bool:
    """Validate AI personality type"""
    valid_personalities = ['supportive', 'sarcastic', 'humorous', 'motivational', 'professional']
    return personality in valid_personalities

def validate_output_format(output_format: str) -> bool:
    """Validate preferred output format"""
    valid_formats = ['text', 'audio', 'video', 'meme']
    return output_format in valid_formats

def sanitize_text(text: str) -> str:
    """Sanitize text input"""
    if not text:
        return ''
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Trim whitespace
    text = text.strip()
    
    return text

def validate_file_upload(file) -> Dict[str, Any]:
    """Validate file upload"""
    if not file:
        return {'valid': False, 'message': 'No file provided'}
    
    if not file.filename:
        return {'valid': False, 'message': 'No filename provided'}
    
    # Check file size (assuming file.content_length is available)
    max_size = 16 * 1024 * 1024  # 16MB
    if hasattr(file, 'content_length') and file.content_length > max_size:
        return {'valid': False, 'message': 'File too large (max 16MB)'}
    
    # Check file extension
    allowed_extensions = {
        'audio': ['.mp3', '.wav', '.ogg', '.m4a'],
        'video': ['.mp4', '.avi', '.mov', '.mkv'],
        'image': ['.jpg', '.jpeg', '.png', '.gif']
    }
    
    file_ext = file.filename.lower().split('.')[-1] if '.' in file.filename else ''
    file_ext = '.' + file_ext
    
    valid_extension = False
    for category, extensions in allowed_extensions.items():
        if file_ext in extensions:
            valid_extension = True
            break
    
    if not valid_extension:
        return {'valid': False, 'message': 'Invalid file type'}
    
    return {'valid': True, 'message': 'File is valid'}

def validate_rating(rating: Any) -> Dict[str, Any]:
    """Validate content rating"""
    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            return {'valid': False, 'message': 'Rating must be between 1 and 5'}
        return {'valid': True, 'message': 'Rating is valid'}
    except (ValueError, TypeError):
        return {'valid': False, 'message': 'Rating must be a number'}
