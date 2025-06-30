"""
Script d'entraînement du modèle de classification des intentions pour le bot WhatsApp.
"""

import os
import pickle
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# === Chemins ===
DATA_PATH = "data/final_dataset_balanced.csv"
ML_DIR = "app/ml"
os.makedirs(ML_DIR, exist_ok=True)

# === Chargement des données ===
print("📥 Chargement du dataset...")
df = pd.read_csv(DATA_PATH)

texts = df["message"].astype(str).tolist()
labels = df["intent"].astype(str).tolist()

# === Encodage des intentions ===
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(labels)
num_classes = len(label_encoder.classes_)

# === Tokenisation
print("🔤 Tokenisation...")
tokenizer = Tokenizer(oov_token="<OOV>")
tokenizer.fit_on_texts(texts)
X = tokenizer.texts_to_sequences(texts)
X = pad_sequences(X)

vocab_size = len(tokenizer.word_index) + 1
input_length = X.shape[1]

# === Split jeu de données
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# === Architecture du modèle
model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=16, input_length=input_length),
    GlobalAveragePooling1D(),
    Dense(32, activation='relu'),
    Dense(num_classes, activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# === Callbacks
callbacks = [
    EarlyStopping(patience=3, restore_best_weights=True),
    ModelCheckpoint(os.path.join(ML_DIR, "best_model.h5"), save_best_only=True)
]

# === Entraînement
print("🚀 Entraînement du modèle...")
history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=30,
    batch_size=16,
    callbacks=callbacks,
    verbose=1
)

# === Sauvegarde du modèle et des ressources
print("💾 Sauvegarde du modèle et des fichiers...")
model.save(os.path.join(ML_DIR, "trained_model.h5"))

with open(os.path.join(ML_DIR, "tokenizer.pkl"), "wb") as f:
    pickle.dump(tokenizer, f)

with open(os.path.join(ML_DIR, "label_classes.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(label_encoder.classes_))

with open(os.path.join(ML_DIR, "label_encoder.pkl"), "wb") as f:
    pickle.dump(label_encoder, f)

# === Résumé
print("✅ Modèle entraîné et sauvegardé avec succès !")
print(f"   • Modèle      : {ML_DIR}/trained_model.h5")
print(f"   • Tokenizer   : {ML_DIR}/tokenizer.pkl")
print(f"   • Classes     : {ML_DIR}/label_classes.txt")
print(f"   • Encodage    : {ML_DIR}/label_encoder.pkl")
