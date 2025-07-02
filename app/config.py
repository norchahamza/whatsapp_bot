# app/config.py

import os
from dotenv import load_dotenv

# 🔄 Charge les variables d'environnement (.env)
load_dotenv()


class Config:
    """Classe de configuration pour les chemins, clés API, et constantes globales."""

    # === Base directories ===
    ROOT_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )  # Racine du projet
    APP_DIR = os.path.join(ROOT_DIR, "app")
    DATA_DIR = os.path.join(ROOT_DIR, "data")
    DB_DIR = os.path.join(APP_DIR, "database")
    ML_DIR = os.path.join(APP_DIR, "ml")
    LOG_DIR = os.path.join(ROOT_DIR, "logs")
    CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))

    # === Fichiers spécifiques ===
    # Ancienne ligne: RESPONSES_FILE = os.path.join(ROOT_DIR, "whatsapp_bot", ".vscode", "response.json")
    RESPONSES_FILE = os.path.join(DATA_DIR, "responses.json") # Nouvelle ligne
    DB_FILE = os.path.join(DB_DIR, "products.db")
    CONVERSATION_LOG = os.path.join(DATA_DIR, "conversation_logs.json")
    AUDIO_LOG = os.path.join(DATA_DIR, "audio_errors.csv")
    FALLBACK_LOG = os.path.join(LOG_DIR, "language_fallback.log")

    # === Fichiers ML ===
    TRAINED_MODEL_FILE = os.path.join(ML_DIR, "trained_model.h5")
    TOKENIZER_FILE = os.path.join(ML_DIR, "tokenizer.pkl")
    LABELS_FILE = os.path.join(ML_DIR, "label_classes.txt")
    LABEL_ENCODER_FILE = os.path.join(ML_DIR, "label_encoder.pkl")

    # === Paramètres généraux ===
    DEBUG = True
    DEFAULT_LANG = "darija"

    # === Credentials ===
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    WHISPER_MODEL_NAME = os.getenv("WHISPER_MODEL_NAME", "medium")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION", "2022-12-01")
    OPENAI_API_MODEL = os.getenv("OPENAI_API_MODEL", "gpt-3.5-turbo")
    OPENAI_API_TEMPERATURE = float(os.getenv("OPENAI_API_TEMPERATURE", "0.5"))
    OPENAI_API_MAX_TOKENS = int(os.getenv("OPENAI_API_MAX_TOKENS", "1000"))
    OPENAI_API_TOP_P = float(os.getenv("OPENAI_API_TOP_P", "1.0"))
    OPENAI_API_FREQUENCY_PENALTY = float(os.getenv("OPENAI_API_FREQUENCY_PENALTY", "0.0"))
