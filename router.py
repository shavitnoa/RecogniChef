def get_source_type(url):
    """
    תת-משימה 1: זיהוי סוג המקור כדי לחסוך במשאבים.
    """
    url = url.lower()
    
    # 1. זיהוי רשתות חברתיות (דורש וידאו - Vision)
    if any(domain in url for domain in ["instagram.com", "tiktok.com", "reels"]):
        return "SOCIAL_VIDEO"
    
    # 2. זיהוי יוטיוב (דורש תמלול - טקסט)
    if any(domain in url for domain in ["youtube.com", "youtu.be"]):
        # אם זה Shorts, לפעמים עדיף להתייחס לזה כוידאו, אבל לרוב תמלול מספיק
        return "YOUTUBE_TRANSCRIPT"
    
    # 3. כל השאר (אתרים - טקסט נקי)
    return "WEB_SCRAPE"

# דוגמה לשימוש:
# source = get_source_type("https://www.instagram.com/p/C123/") 
# print(source) -> SOCIAL_VIDEO