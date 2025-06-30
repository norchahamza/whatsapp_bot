# app/utils/intent_classifier.py
import os
import pickle
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# 📦 Chargement centralisé des réponses
from app.utils.response_utils import get_response

# === Chemins des modèles ===
model_path = os.path.join(os.path.dirname(__file__), 'intent_model.pkl')
vec_path = os.path.join(os.path.dirname(__file__), 'vectorizer.pkl')

# 🧠 Cache du modèle et du vectorizer
_model = None
_vectorizer = None

def load_intent_model():
    global _model, _vectorizer
    if _model is None or _vectorizer is None:
        with open(model_path, 'rb') as f:
            _model = pickle.load(f)
        with open(vec_path, 'rb') as f:
            _vectorizer = pickle.load(f)
    return _model, _vectorizer

# 🎯 Détection de l’intention
def detect_intent(text, lang="darija"):
    if not os.path.exists(model_path) or not os.path.exists(vec_path):
        print("❌ Modèle d'intention non entraîné. Veuillez exécuter intent_trainer.py")
        return "fallback", get_response("fallback", lang)

    try:
        model, vectorizer = load_intent_model()
        X = vectorizer.transform([text])
        intent = model.predict(X)[0]
        print(f"[INTENT] '{text}' → intention détectée : '{intent}'")

        response = get_response(intent, lang)
        if response:
            return intent, response
        else:
            print(f"⚠️ Intention détectée '{intent}' mais pas de réponse pour la langue '{lang}'")
            return intent, get_response("fallback", lang)

    except Exception as e:
        print("⚠️ Erreur vectorisation :", e)

        # 🔁 Fallback : tentative de matching proche
        try:
            model, _ = load_intent_model()
            for mot in text.lower().split():
                match = difflib.get_close_matches(mot, model.classes_, n=1, cutoff=0.6)
                if match:
                    intent = match[0]
                    print(f"[FALLBACK MATCH] Mot '{mot}' → intention '{intent}'")
                    return intent, get_response(intent, lang)
        except Exception as fallback_error:
            print("⚠️ Erreur fallback matching :", fallback_error)

        return "fallback", get_response("fallback", lang)
