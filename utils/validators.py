# video_scraper_project/utils/validators.py

import re
from config import BRAND_KEYWORDS

def is_brand_related(text):
    """Check if text contains brand-related keywords"""
    if not text:
        return False
    
    text_lower = text.lower()
    for keyword in BRAND_KEYWORDS:
        if keyword.lower() in text_lower:
            return True
    
    # Check for hashtags
    hashtags = re.findall(r"#(\w+)", text)
    for tag in hashtags:
        if any(keyword.lower() in tag.lower() for keyword in BRAND_KEYWORDS):
            return True
    
    return False

def filter_video_metadata(metadata):
    """Filter video metadata to ensure it's brand-related"""
    # Check title, description, and tags for brand relevance
    relevant_fields = [
        metadata.get('title', ''),
        metadata.get('description', ''),
        metadata.get('tags', ''),
        ' '.join(metadata.get('hashtags', []))
    ]
    
    combined_text = ' '.join(str(field) for field in relevant_fields)
    return is_brand_related(combined_text)