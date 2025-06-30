"""Module principal du bot WhatsApp utilisant Flask et Twilio."""

import difflib
import json
import re
import os
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from config import Config
from app.utils.response_utils import get_response
from app.database.db_manager import get_all_products
from app.handlers.audio_handler_whisper import download_and_transcribe_audio
from app.utils.lang_detect import detect_language, post_process_lang
from app.utils.logger import log_conversation, log_language_fallback
from app.utils.intent_classifier import detect_intent
from app.utils.preprocessing import normaliser_darija
from app.utils.history_manager import ConversationHistoryManager 
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


app = Flask(__name__)
conversation_history_manager = ConversationHistoryManager()


def _initialize_user_session(user_id):
    """Initialise la session utilisateur si elle n'existe pas."""
    if not conversation_history_manager.has_user(user_id):
        conversation_history_manager.init_user(user_id)


def sauvegarder_historique():
    """Fonction de sauvegarde de l'historique (placeholder)."""
    pass


def corriger_mots_proches(phrase):
    """Corrige les mots proches dans une phrase selon les noms de produits."""
    produits = [p[1].lower() for p in get_all_products()]
    mots = phrase.lower().split()
    corriges = mots.copy()
    i = 0
    while i < len(mots):
        correction_trouvee = False
        for j in range(3, 0, -1):
            if i + j <= len(mots):
                segment = " ".join(mots[i:i + j])
                match = difflib.get_close_matches(segment, produits, n=1, cutoff=0.7)
                if match:
                    corriges[i:i + j] = [match[0]] + [""] * (j - 1)
                    i += j
                    correction_trouvee = True
                    break
        if not correction_trouvee:
            i += 1
    return " ".join([w for w in corriges if w])


def contient_produit(phrase):
    """Vérifie si une phrase contient un produit connu."""
    noms_produits = [p[1].lower() for p in get_all_products()]
    mots = re.findall(r'\w+', phrase.lower())
    for mot in mots:
        for nom in noms_produits:
            if difflib.SequenceMatcher(None, mot, nom).ratio() > 0.7:
                return nom
    return None


def _handle_empty_message(user_id, resp, lang):
    """Gère les messages vides."""
    response = get_response("empty_message", lang) or "❌ Message vide reçu."
    msg = resp.message()
    msg.body(response)
    conversation_history_manager.get_user_history(user_id)["messages"].append({"from": "bot", "text": response})
    log_conversation(user_id, "[vide]", response, "empty_message")
    sauvegarder_historique()


def _handle_audio_message(request, user_id, lang):
    """Gère les messages audio en les transcrivant."""
    audio_url = request.values.get("MediaUrl0")
    transcribed_text, audio_lang = download_and_transcribe_audio(audio_url)
    if not transcribed_text or transcribed_text.startswith("[Erreur transcription vocale"):
        fallback_message = "❌ Une erreur est survenue lors de la transcription audio."
        resp = MessagingResponse()
        resp.message(fallback_message)
        log_conversation(user_id, "[audio]", fallback_message, "audio_transcription_error", lang)
        sauvegarder_historique()
        return None, lang, str(resp)
    return transcribed_text, post_process_lang(transcribed_text, audio_lang), None


def _handle_message_logic(incoming_msg, request, user_id):
    """Détecte la langue, normalise le message et applique les corrections."""
    lang = "darija"
    if not incoming_msg and not request.values.get("NumMedia"):
        return None, lang, "empty_message"

    if request.values.get("NumMedia") and request.values.get("MediaContentType0", "").startswith("audio"):
        transcribed_text, audio_lang, audio_error_response = _handle_audio_message(request, user_id, lang)
        if transcribed_text is None:
            return None, lang, audio_error_response
        incoming_msg = transcribed_text
        lang = audio_lang
        detected = detect_language(incoming_msg.lower())
        lang = detected if detected in ['fr', 'en', 'darija'] else 'darija'
        if audio_lang != lang:
            log_language_fallback(user_id, transcribed_text, audio_lang, lang, source="audio")
    else:
        try:
            detected = detect_language(incoming_msg.lower())
            lang = detected if detected in ['fr', 'en', 'darija'] else 'darija'
        except Exception:
            lang = 'darija'

    if lang == "darija":
        incoming_msg = normaliser_darija(incoming_msg)

    incoming_msg = corriger_mots_proches(incoming_msg)
    return incoming_msg, lang, None


def segment_text(text):
    """Segmente un texte long en plusieurs morceaux sémantiques."""
    if len(text.strip().split()) <= 3:
        return [text.strip()]
    return [s.strip() for s in re.split(r'[.,;!?]| et | puis | mais ', text) if s.strip()]


def detect_intent_and_response(message, lang):
    """Détecte l'intention et retourne une réponse selon la langue."""
    intent, response = detect_intent(message, lang)
    prioritaires = ["greeting", "thanks", "help"]
    if intent in prioritaires:
        return intent, get_response(intent, lang)
    if not intent:
        return None, get_response("fallback", lang)
    if not response:
        return intent, get_response("fallback", lang)
    return intent, response


def _handle_multi_intents(message, lang, user_id):
    """Gère les intentions multiples dans un message utilisateur."""
    responses = []
    fallback_used = False
    history = conversation_history_manager.get_user_history(user_id)
    last_intent = history.get("last_intent")

    if last_intent == "waiting_quantite":
        message_clean = message.strip().lower()
        nombre_map = {
            "un": 1, "wahd": 1, "1": 1,
            "deux": 2, "jouj": 2, "joujat": 2, "tnin": 2, "2": 2,
            "trois": 3, "tleta": 3, "3": 3,
            "quatre": 4, "rb3a": 4, "4": 4,
            "cinq": 5, "khmsa": 5, "5": 5,
            "six": 6, "sitta": 6, "6": 6,
            "sept": 7, "sb3a": 7, "7": 7,
            "huit": 8, "tmnya": 8, "8": 8,
            "neuf": 9, "ts3ud": 9, "9": 9,
            "dix": 10, "3achra": 10, "10": 10
        }
        try:
            quantite = int(message_clean)
        except ValueError:
            quantite = nombre_map.get(message_clean, None)

        if quantite:
            response = get_response("confirmation_yes", lang)
            conversation_history_manager.update_last_interaction(user_id, intent=None, response=response)
            return response
        return get_response("ask_quantity", lang)

    for segment in segment_text(message):
        intent, _ = detect_intent(segment, lang)
        if intent:
            response = get_response(intent, lang)
            if response and response not in responses:
                responses.append(response)
            elif get_response("fallback", lang) not in responses:
                responses.append(get_response("fallback", lang))
                fallback_used = True

    if not responses:
        return get_response("fallback", lang)

    if fallback_used:
        responses.append("🤖 J’ai fait de mon mieux pour comprendre votre demande.")

    return " • ".join(responses)


@app.route('/webhook', methods=['POST'])
def whatsapp_webhook():
    """Webhook principal appelé par Twilio."""
    original_msg = request.values.get('Body', '').strip()
    user_id = request.values.get('From')
    _initialize_user_session(user_id)

    resp = MessagingResponse()
    incoming_msg, lang, audio_error_response = _handle_message_logic(original_msg, request, user_id)

    if audio_error_response:
        if "<Response>" in audio_error_response:
            return Response(audio_error_response, mimetype='application/xml')
        resp.message(get_response("fallback", lang))
        return Response(str(resp), mimetype='application/xml')

    if not incoming_msg:
        _handle_empty_message(user_id, resp, lang)
        return str(resp)

    multi_intent_response = _handle_multi_intents(incoming_msg, lang, user_id)
    resp.message(multi_intent_response)

    conversation_history_manager.update_last_interaction(user_id, intent=None, response=multi_intent_response)
    conversation_history_manager.add_message(user_id, "user", incoming_msg)
    conversation_history_manager.add_message(user_id, "bot", multi_intent_response)
    log_conversation(user_id, incoming_msg, multi_intent_response, "multi_intent", lang)
    sauvegarder_historique()

    return Response(str(resp), mimetype="application/xml")


@app.route('/')
def index():
    """Page d'accueil basique de l'API."""
    return "Bienvenue sur l'API WhatsApp Bot ! Envoyez un message pour commencer."


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
