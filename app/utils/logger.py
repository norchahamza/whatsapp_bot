#app\utils\logger.py
import csv
import os
from datetime import datetime
lang_log_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "lang_detection_fallback_log.csv")

csv_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "conversation_dataset.csv")

def log_conversation(user_id, message, response, intent, lang="unknown"):
    file_exists = os.path.isfile(csv_path)

    with open(csv_path, mode="a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["datetime", "user_id", "message", "response", "intent", "lang"])
        
        writer.writerow([datetime.now(), user_id, message, response, intent, lang])
# Chemin du fichier de log linguistique

def log_language_fallback(user_id, transcribed_text, original_lang, corrected_lang, source="audio"):
    """
    Journalise les cas où la langue détectée automatiquement est corrigée manuellement.
    """
    file_exists = os.path.isfile(lang_log_path)

    with open(lang_log_path, mode="a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "user_id", "transcribed_text", "original_lang", "corrected_lang", "source"])
        writer.writerow([datetime.now(), user_id, transcribed_text, original_lang, corrected_lang, source])
