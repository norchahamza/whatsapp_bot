#app/utils/intent_trainer.py
import os
import pickle
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from app.utils.response_utils import get_response

# 📁 Chemins vers les fichiers du modèle
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, 'intent_model.pkl')
VEC_PATH = os.path.join(BASE_DIR, 'vectorizer.pkl')

# 🔁 Cache modèle en mémoire (utile pour éviter rechargement répété)
_model = None
_vectorizer = None

def _load_model():
    global _model, _vectorizer
    if _model is None or _vectorizer is None:
        if not os.path.exists(MODEL_PATH) or not os.path.exists(VEC_PATH):
            raise FileNotFoundError("📦 Modèle non trouvé. Veuillez exécuter le script d'entraînement.")
        with open(MODEL_PATH, 'rb') as f:
            _model = pickle.load(f)
        with open(VEC_PATH, 'rb') as f:
            _vectorizer = pickle.load(f)
    return _model, _vectorizer


def detect_intent(text, lang="darija"):
    """
    Prédit l'intention depuis un texte utilisateur. Retourne aussi la réponse.
    Utilise fallback si le modèle échoue ou si aucune réponse trouvée.
    """
    try:
        model, vectorizer = _load_model()
        X = vectorizer.transform([text])
        intent = model.predict(X)[0]

        response = get_response(intent, lang)
        if response:
            return intent, response
        else:
            print(f"⚠️ Réponse manquante pour l’intention '{intent}' et la langue '{lang}'")
            return intent, get_response("fallback", lang)

    except Exception as e:
        print("⚠️ Erreur détection d’intention :", e)

        # 🔁 Fallback via matching sur classes
        try:
            model, _ = _load_model()
            for mot in text.lower().split():
                match = difflib.get_close_matches(mot, model.classes_, n=1, cutoff=0.6)
                if match:
                    intent = match[0]
                    return intent, get_response(intent, lang)
        except Exception as fallback_error:
            print("⚠️ Fallback échoué :", fallback_error)

        return "fallback", get_response("fallback", lang)


def train_intent_model(data, labels):
    """
    Entraîne un modèle de classification d’intentions depuis des données texte + labels.
    Sauvegarde le modèle et le vectorizer dans le dossier local.
    """
    try:
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(data)

        model = LogisticRegression(max_iter=1000)
        model.fit(X, labels)

        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(model, f)
        with open(VEC_PATH, 'wb') as f:
            pickle.dump(vectorizer, f)

        print("✅ Modèle entraîné et sauvegardé dans :", MODEL_PATH)
        print("✅ Vectorizer sauvegardé dans :", VEC_PATH)

    except Exception as e:
        print("❌ Erreur entraînement modèle :", e)


# 🧪 Test manuel (debug local)
if __name__ == "__main__":
    test_text = "Salam"
    intent, response = detect_intent(test_text)
    print(f"🧠 Intent: {intent} → 💬 Réponse: {response}")
# app/utils/intent_trainer.py