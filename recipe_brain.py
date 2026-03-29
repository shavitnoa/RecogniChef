from google import genai
from google.genai import types
import json
import time

class RecipeBrain:
    def __init__(self, api_key):
        """
        שימוש בספריה החדשה google-genai.
        המפתח מוזרק מה-Backend לטובת אבטחה.
        """
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-3.1-flash-lite-preview" 
        
        self.system_instruction = """
        אתה סוכן 'מחלץ מתכונים' מומחה.
        תפקידך: חילוץ מתכון מדויק מתוך מידע גולמי (טקסט או וידאו).
        
        דגשים:
        1. חלץ שם מנה, מצרכים עם כמויות ושלבי הכנה.
        2. בוידאו: זהה מצרכים ויזואלית וקרא כתוביות על המסך.
        3. החזר אך ורק JSON נקי.
        """

    def process(self, raw_input, is_video=False):
        try:
            if is_video:
                # העלאת קובץ בספריה החדשה
                video_file = self.client.files.upload(path=raw_input)
                
                # המתנה לסיום עיבוד
                while video_file.state == "PROCESSING":
                    time.sleep(2)
                    video_file = self.client.files.get(name=video_file.name)
                
                # יצירת התוכן מהוידאו
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=[video_file, "נתח את הוידאו וחלץ מתכון."],
                    config=types.GenerateContentConfig(
                        system_instruction=self.system_instruction,
                        response_mime_type="application/json"
                    )
                )
            else:
                # עיבוד טקסט ישיר
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=f"חלץ מתכון מהטקסט הבא: {raw_input}",
                    config=types.GenerateContentConfig(
                        system_instruction=self.system_instruction,
                        response_mime_type="application/json"
                    )
                )
            
            return response.text

        except Exception as e:
            return json.dumps({"error": f"Brain Error: {str(e)}"})