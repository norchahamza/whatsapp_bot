# app/ml/model_loader.py
# pyright: strict
# pyright: reportMissingImports=false

import os
import pickle
import numpy as np
import tensorflow as tf

from typing import List
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

class ModelLoader:
    def __init__(
        self,
        model_path: str = "app/ml/trained_model.h5",
        tokenizer_path: str = "app/ml/tokenizer.pkl",
        labels_path: str = "app/ml/label_classes.txt",
        max_len: int = 20
    ) -> None:
        self.model_path = model_path
        self.tokenizer_path = tokenizer_path
        self.labels_path = labels_path
        self.max_len = max_len

        self.model: Model | None = None
        self.tokenizer: Tokenizer | None = None
        self.labels: List[str] = []

        self.load_all()

    def load_all(self) -> None:
        if os.path.exists(self.model_path):
            self.model = tf.keras.models.load_model(self.model_path)
            print(f"✅ Modèle chargé depuis {self.model_path}")
        else:
            raise FileNotFoundError(f"❌ Modèle introuvable à {self.model_path}")

        if os.path.exists(self.tokenizer_path):
            with open(self.tokenizer_path, "rb") as f:
                self.tokenizer = pickle.load(f)
            print(f"✅ Tokenizer chargé depuis {self.tokenizer_path}")
        else:
            raise FileNotFoundError(f"❌ Tokenizer introuvable à {self.tokenizer_path}")

        if os.path.exists(self.labels_path):
            with open(self.labels_path, "r", encoding="utf-8") as f:
                self.labels = [line.strip() for line in f]
            print(f"✅ Labels chargés depuis {self.labels_path}")
        else:
            raise FileNotFoundError(f"❌ Labels introuvables à {self.labels_path}")

    def predict_response(self, user_message: str) -> str:
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Modèle ou tokenizer non chargé.")
        sequence = self.tokenizer.texts_to_sequences([user_message])
        padded = pad_sequences(sequence, maxlen=self.max_len, padding='post')
        probabilities = self.model.predict(padded, verbose=0)
        return self.labels[int(np.argmax(probabilities))]
