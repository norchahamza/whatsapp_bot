#app\ml\train_model.py
import pandas as pd
from app.ml.model import NeuralResponseModel
import pickle
# Initialise le modèle
model = NeuralResponseModel()

# Charger le dataset
df = pd.read_csv("data/conversation_dataset.csv")
texts = df["message"].astype(str).tolist()
responses = df["response"].astype(str).tolist()

# Entraîner le modèle
model.build_and_train(texts, responses)

# Sauvegarde
model.model.save("app/ml/trained_model.h5")
print("✅ Modèle entraîné et sauvegardé dans app/ml/trained_model.h5")


# Sauvegarde du tokenizer
with open("app/ml/tokenizer.pkl", "wb") as f:
    pickle.dump(model.tokenizer, f)

# Sauvegarde des classes (responses)
with open("app/ml/label_classes.txt", "w", encoding="utf-8") as f:
    for label in model.responses:
        f.write(label + "\n")

print("✅ Tokenizer et classes sauvegardés.")