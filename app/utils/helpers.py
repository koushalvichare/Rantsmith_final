from datetime import datetime
import hashlib
import uuid
import os
from typing import Any, Dict, List

def generate_unique_filename(original_filename: str, user_id: int) -> str:
    """Generate a unique filename for uploads"""
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    file_ext = os.path.splitext(original_filename)[1]
    unique_id = str(uuid.uuid4())[:8]
    
    return f"user_{user_id}_{timestamp}_{unique_id}{file_ext}"

def hash_content(content: str) -> str:
    """Generate hash for content deduplication"""
    return hashlib.sha256(content.encode()).hexdigest()

def format_timestamp(timestamp: datetime) -> str:
    """Format timestamp for display"""
    if not timestamp:
        return "N/A"
    
    now = datetime.utcnow()
    diff = now - timestamp
    
    if diff.days > 7:
        return timestamp.strftime("%Y-%m-%d")
    elif diff.days > 0:
        return f"{diff.days} days ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hours ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minutes ago"
    else:
        return "Just now"

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """Extract keywords from text (simple implementation)"""
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
        'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after',
        'above', 'below', 'between', 'among', 'is', 'are', 'was', 'were', 'be', 'been',
        'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'shall', 'can', 'cannot', 'i', 'you', 'he',
        'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your',
        'his', 'her', 'its', 'our', 'their', 'this', 'that', 'these', 'those'
    }
    
    # Clean and split text
    import re
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    
    # Filter out stop words and short words
    keywords = [word for word in words if word not in stop_words and len(word) > 3]
    
    # Count word frequency
    word_count = {}
    for word in keywords:
        word_count[word] = word_count.get(word, 0) + 1
    
    # Sort by frequency and return top keywords
    sorted_keywords = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    return [word for word, count in sorted_keywords[:max_keywords]]

def calculate_readability_score(text: str) -> float:
    """Calculate simple readability score (0-1, higher is more readable)"""
    if not text:
        return 0.0
    
    # Simple metrics
    sentences = text.split('.')
    words = text.split()
    
    if len(sentences) == 0 or len(words) == 0:
        return 0.0
    
    avg_words_per_sentence = len(words) / len(sentences)
    avg_chars_per_word = sum(len(word) for word in words) / len(words)
    
    # Simple scoring (adjust weights as needed)
    score = 1.0
    
    # Penalize very long sentences
    if avg_words_per_sentence > 20:
        score -= 0.2
    
    # Penalize very long words
    if avg_chars_per_word > 6:
        score -= 0.1
    
    return max(0.0, min(1.0, score))

def format_emotion_confidence(confidence: float) -> str:
    """Format emotion confidence for display"""
    if confidence >= 0.8:
        return "Very confident"
    elif confidence >= 0.6:
        return "Confident"
    elif confidence >= 0.4:
        return "Somewhat confident"
    else:
        return "Low confidence"

def format_sentiment_score(score: float) -> str:
    """Format sentiment score for display"""
    if score >= 0.5:
        return "Positive"
    elif score >= 0.1:
        return "Slightly positive"
    elif score >= -0.1:
        return "Neutral"
    elif score >= -0.5:
        return "Slightly negative"
    else:
        return "Negative"

def create_response_metadata(processing_time: float, model_used: str, quality_score: float) -> Dict[str, Any]:
    """Create metadata for AI responses"""
    return {
        'processing_time': round(processing_time, 2),
        'model_used': model_used,
        'quality_score': round(quality_score, 2),
        'timestamp': datetime.utcnow().isoformat(),
        'performance_rating': 'excellent' if quality_score >= 0.8 else 'good' if quality_score >= 0.6 else 'average'
    }

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove or replace unsafe characters
    import re
    # Keep only alphanumeric characters, dots, hyphens, and underscores
    safe_filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    # Limit length
    if len(safe_filename) > 100:
        name, ext = os.path.splitext(safe_filename)
        safe_filename = name[:95] + ext
    return safe_filename

def parse_json_safely(json_string: str) -> Any:
    """Safely parse JSON string"""
    try:
        import json
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError):
        return None

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    
    return f"{s} {size_names[i]}"
