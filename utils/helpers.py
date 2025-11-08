"""
Helper functions for BRD Generator
"""

import re
import os
from typing import List, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """
    Clean and normalize text content
    
    Args:
        text: Input text to clean
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters that might cause issues
    text = re.sub(r'[^\w\s\-\.\,\:\;\(\)\[\]\/\&\@]', '', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text

def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted file size string
    """
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def generate_unique_id() -> str:
    """
    Generate a unique ID based on timestamp
    
    Returns:
        Unique ID string
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"BRD_{timestamp}"

def safe_filename(filename: str) -> str:
    """
    Create a safe filename by removing invalid characters
    
    Args:
        filename: Original filename
        
    Returns:
        Safe filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    
    # Remove multiple underscores
    filename = re.sub(r'_+', '_', filename)
    
    # Remove leading/trailing underscores
    filename = filename.strip('_')
    
    # Limit length
    if len(filename) > 100:
        filename = filename[:100]
    
    return filename

def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """
    Extract keywords from text
    
    Args:
        text: Text to extract keywords from
        min_length: Minimum length of keywords
        
    Returns:
        List of keywords
    """
    if not text:
        return []
    
    # Convert to lowercase and split into words
    words = text.lower().split()
    
    # Filter out common words and short words
    common_words = {
        'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
        'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before',
        'after', 'above', 'below', 'between', 'among', 'this', 'that', 'these',
        'those', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
        'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
        'may', 'might', 'must', 'can', 'shall', 'a', 'an', 'as', 'if', 'it',
        'its', 'it', 'we', 'you', 'they', 'them', 'their', 'what', 'which',
        'who', 'whom', 'when', 'where', 'why', 'how', 'i', 'me', 'my', 'your'
    }
    
    keywords = []
    for word in words:
        # Remove punctuation
        word = re.sub(r'[^\w]', '', word)
        
        # Check conditions
        if (len(word) >= min_length and 
            word not in common_words and 
            word.isalpha()):
            keywords.append(word)
    
    # Remove duplicates and return
    return list(set(keywords))

def calculate_readability_score(text: str) -> float:
    """
    Calculate a simple readability score
    
    Args:
        text: Text to analyze
        
    Returns:
        Readability score between 0 and 1
    """
    if not text:
        return 0.0
    
    # Split into sentences
    sentences = text.split('.')
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return 0.0
    
    # Calculate average sentence length
    total_words = sum(len(s.split()) for s in sentences)
    avg_sentence_length = total_words / len(sentences)
    
    # Simple scoring based on sentence length
    # Optimal sentence length is 15-20 words
    if 15 <= avg_sentence_length <= 20:
        return 1.0
    elif 10 <= avg_sentence_length < 15 or 20 < avg_sentence_length <= 25:
        return 0.8
    elif 5 <= avg_sentence_length < 10 or 25 < avg_sentence_length <= 30:
        return 0.6
    else:
        return 0.4

def create_directory_if_not_exists(directory_path: str) -> bool:
    """
    Create directory if it doesn't exist
    
    Args:
        directory_path: Path to create
        
    Returns:
        True if successful, False otherwise
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Failed to create directory {directory_path}: {str(e)}")
        return False

def get_file_extension(filename: str) -> str:
    """
    Get file extension from filename
    
    Args:
        filename: Filename to extract extension from
        
    Returns:
        File extension (including dot)
    """
    return os.path.splitext(filename)[1].lower()

def is_valid_domain(domain: str, supported_domains: List[str]) -> bool:
    """
    Validate if domain is supported
    
    Args:
        domain: Domain to validate
        supported_domains: List of supported domains
        
    Returns:
        True if valid, False otherwise
    """
    return domain in supported_domains

def format_percentage(value: float, decimal_places: int = 2) -> str:
    """
    Format value as percentage
    
    Args:
        value: Value to format (0-1)
        decimal_places: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    return f"{value * 100:.{decimal_places}f}%"

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to specified length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge two dictionaries
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary
        
    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    result.update(dict2)
    return result

def get_current_timestamp() -> str:
    """
    Get current timestamp as string
    
    Returns:
        Timestamp string
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_performance(func_name: str, start_time: float, end_time: float):
    """
    Log performance metrics
    
    Args:
        func_name: Name of the function
        start_time: Start time
        end_time: End time
    """
    duration = end_time - start_time
    logger.info(f"Performance: {func_name} took {duration:.2f} seconds")

def validate_json_structure(data: Dict[str, Any], required_keys: List[str]) -> bool:
    """
    Validate JSON structure has required keys
    
    Args:
        data: Dictionary to validate
        required_keys: List of required keys
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(data, dict):
        return False
    
    for key in required_keys:
        if key not in data:
            return False
    
    return True