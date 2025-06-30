#app/utils/lang_detect.py
from langdetect import detect
import unicodedata
from datetime import datetime

def _normalize_text(text):
    text = text.strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join([c for c in text if not unicodedata.combining(c)])
    return text

def detect_language(text):
    try:
        lang = detect(text)
        if lang == 'fr':
            return 'fr'
        elif lang == 'en':
            return 'en'
        else:
            return 'darija'  # fallback générique
    except:
        return 'darija'

def post_process_lang(transcribed_text, audio_lang):
    """
    Corrige la langue détectée automatiquement par Whisper si elle est probablement erronée.
    """
    text = _normalize_text(transcribed_text)

    darija_salutations = {
        "salam", "slm", "salut", "salaam", "salam alikoum",
        "السلام", "سلام", "السلام عليكم", "سلاااام"
    }

    darija_keywords = {"afak", "wach", "bghit", "kifach", "sh7al", "fin", "labas", "zouine"}

    if audio_lang.startswith("fr") and (text in darija_salutations or any(kw in text for kw in darija_keywords)):
        print("🔁 Correction de langue : Whisper a détecté 'fr', mais c’est probablement du darija.")
        return "darija"

    if audio_lang.startswith('fr'):
        return "fr"
    elif audio_lang in ['ar', 'ma']:
        return "darija"
    else:
        return "en"

def log_language_fallback(user_id, text, detected_lang, fallback_lang, source="text"):
    """
    Enregistre un log de la langue détectée et de la langue de fallback utilisée.
    """
    print(f"[LANGUAGE FALLBACK] User {user_id}: '{text}' → Langue détectée: {detected_lang}, Langue fallback: {fallback_lang} (source: {source})")
    
    # ✅ Logging avec horodatage
    with open("language_fallback.log", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] User {user_id}: '{text}' → Langue détectée: {detected_lang}, Langue fallback: {fallback_lang} (source: {source})\n")
    return fallback_lang