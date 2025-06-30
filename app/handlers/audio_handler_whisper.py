#app/handlers/audio_handler_whisper.py
import os
import tempfile
import whisper
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from datetime import datetime

# Charger les variables d'environnement
load_dotenv()
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

# Charger le modèle Whisper une seule fois
model = whisper.load_model("medium")

# Dossier de log d'erreur
LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "audio_errors.csv")

def log_audio_error(message, url=""):
    try:
        from csv import writer
        if not os.path.exists(LOG_PATH) or os.stat(LOG_PATH).st_size == 0:
            with open(LOG_PATH, "a", encoding="utf-8", newline="") as f:
                w = writer(f)
                w.writerow(["timestamp", "error", "media_url"])
        with open(LOG_PATH, "a", encoding="utf-8", newline="") as f:
            w = writer(f)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            w.writerow([timestamp, message, url])
    except Exception as e:
        print("⚠️ Échec log_audio_error :", e)

def download_and_transcribe_audio(media_url):
    tmp_audio_path = None
    try:
        if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
            raise Exception("❌ SID ou TOKEN manquant. Vérifie ton fichier .env")

        response = requests.get(media_url, auth=HTTPBasicAuth(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN), timeout=10)
        if response.status_code != 200:
            raise Exception(f"Code {response.status_code} pendant téléchargement audio")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
            tmp_audio.write(response.content)
            tmp_audio_path = tmp_audio.name
        result = model.transcribe(tmp_audio_path)  # ⬅️ langue auto
        text_result = result.get("text", "")
        if isinstance(text_result, list):
            transcription = " ".join(text_result).strip()
        else:
            transcription = str(text_result).strip()
        detected_lang = result.get("language", "fr")
        if not transcription:
            raise Exception("Transcription vide ou invalide")
        if detected_lang not in ["fr", "ar", "en"]:
            detected_lang = "fr"
        print("📢 Transcription Whisper:", transcription)
        print("🌐 Langue détectée:", detected_lang)
        return transcription, detected_lang
    except Exception as e:
        log_audio_error(str(e), media_url)
        return f"[Erreur transcription vocale: {str(e)}]", "fr"
    finally:
        if tmp_audio_path and os.path.exists(tmp_audio_path):
            try:
                os.remove(tmp_audio_path)
            except Exception as cleanup_error:
                log_audio_error(f"Suppression temp échouée: {cleanup_error}")
                print("⚠️ Échec de la suppression du fichier temporaire :", cleanup_error)