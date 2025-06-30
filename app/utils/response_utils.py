# app/utils/response_utils.py

import os
import json
from app.config import Config

# 📁 Chemin vers le fichier responses.json
responses_path = Config.RESPONSES_FILE
print("➡️ Chargement depuis :", responses_path)

# 🔁 Chargement du fichier responses.json
try:
  with open(responses_path, 'r', encoding='utf-8') as file:
        intent_responses = json.load(file)
except Exception as e:
    print("❌ Erreur lors du chargement de responses.json :", e)
    intent_responses = {}

# ✅ Fonction principale
def get_response(intent, lang="darija"):
    data = intent_responses.get(intent)

    if isinstance(data, str):
        return data

    if isinstance(data, dict):
        response = data.get(lang) or data.get("darija") or data.get("fr")
        if response:
            return response
        else:
            print(f"⚠️ Réponse introuvable pour intent='{intent}' en langue='{lang}'. Fallback utilisé.")

    # Fallback multilingue
    fallback = intent_responses.get("fallback", {}).get(lang)
    if fallback:
        return fallback

    # Dernier recours
    return "❓ Je n'ai pas de réponse pour cette intention."
# 🔎 Test local rapide
if __name__ == "__main__":
    test_cases = [
        ("greeting", "fr"),
        ("merci", "darija"),
        ("commande_invalide", "en"),  # intention inexistante
        ("greeting", "xx"),           # langue inconnue
    ]

    for intent, lang in test_cases:
        print(f"Intent: '{intent}', Langue: '{lang}' → Réponse: {get_response(intent, lang)}")
