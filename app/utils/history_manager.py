# file: app/utils/history_manager.py

import json
import os
from datetime import datetime

CONVERSATION_LOGS_FILE = "conversation_logs.json"

class ConversationHistoryManager:
    def __init__(self):
        self.conversation_history = self._load_history()

    def _load_history(self):
        if os.path.exists(CONVERSATION_LOGS_FILE):
            try:
                with open(CONVERSATION_LOGS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Erreur de chargement du fichier d'historique : {e}")
        return {}
    def has_user(self, user_id):
        return user_id in self.conversation_history

    def init_user(self, user_id):
        self.conversation_history[user_id] = {
            "messages": [],
            "last_intent": None,
            "last_response": None,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def get_user_history(self, user_id):
        if user_id not in self.conversation_history:
            self.init_user(user_id)
        return self.conversation_history[user_id]

    def add_message(self, user_id, msg_type, text):
        self.get_user_history(user_id)["messages"].append({
            "from": msg_type,
            "text": text,
            "timestamp": datetime.now().isoformat()
        })

    def update_last_interaction(self, user_id, intent=None, response=None):
        history = self.get_user_history(user_id)
        if intent is not None:
            history["last_intent"] = intent
        if response is not None:
            history["last_response"] = response

    def save_history(self):
        try:
            with open(CONVERSATION_LOGS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Erreur lors de l'enregistrement de l'historique : {e}")