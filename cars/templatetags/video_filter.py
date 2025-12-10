# cars/templatetags/video_filter.py
from django import template
import re

register = template.Library()

@register.filter
def replace(url):
    """
    Accepts a standard YouTube URL and returns the clean embed URL.
    Handles 'watch?v=' and 'youtu.be/' formats.
    Returns None if no valid ID is found.
    """
    if not url:
        return None

    # Təmiz VIDEO_ID-ni tapmaq üçün regex istifadə edin
    # 1. Uzun format: watch?v=ID (Query string daxilindəki ID)
    # 2. Qısa format: youtu.be/ID (Path daxilindəki ID)
    
    # Bu regex hər iki formatdan ID-ni çıxarır
    video_id_match = re.search(
        r'(?:youtu\.be\/|v=|embed\/|watch\?v=)([^&]+)',
        url
    )
    
    if video_id_match:
        video_id = video_id_match.group(1)
        # Təmiz embed URL-i qaytarın
        return f"https://www.youtube.com/embed/{video_id}"
        
    return None # Əgər heç bir uyğun ID tapılmasa, None qaytarılır