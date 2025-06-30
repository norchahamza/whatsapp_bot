#app\ml\model.py
import numpy as np
from typing import List, Optional
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, GlobalAveragePooling1D, Dense
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

class NeuralResponseModel:
    def __init__(self, num_classes: Optional[int] = None) -> None:
        self.tokenizer: Tokenizer = Tokenizer(oov_token="<OOV>")
        self.model: Optional[Sequential] = None
        self.responses: List[str] = []
        self.num_classes = num_classes

    def pad(self, sequences: List[List[int]], max_len: int = 20) -> np.ndarray:
        return pad_sequences(sequences, maxlen=max_len, padding='post')

    def encode(self, texts: List[str], max_len: int = 20) -> np.ndarray:
        sequences = self.tokenizer.texts_to_sequences(texts)
        return self.pad(sequences, max_len)

    def build_and_train(
        self,
        texts: List[str],
        labels: List[int],
        num_words: int = 1000,
        max_len: int = 20,
        epochs: int = 10
    ) -> None:
        print("🚀 Préparation des données...")
        self.tokenizer.fit_on_texts(texts)
        padded_sequences = self.encode(texts, max_len)

        print("🧠 Construction du modèle...")
        output_dim = self.num_classes if self.num_classes is not None else len(set(labels))

        self.model = Sequential([
            Embedding(input_dim=num_words, output_dim=64, input_length=max_len),
            GlobalAveragePooling1D(),
            Dense(64, activation='relu'),
            Dense(32, activation='relu'),
            Dense(output_dim, activation='softmax')
        ])

        # ✳️ Ignore type warning ici si Pylance le bloque
        self.model.compile(  # type: ignore[attr-defined]
            loss='sparse_categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy']
        )

        print("🎓 Entraînement du modèle...")
        self.model.fit(  # type: ignore[attr-defined]
            padded_sequences, np.array(labels), epochs=epochs, verbose=1
        )

    def predict(self, text: str, max_len: int = 20) -> str:
        if self.model is None:
            raise RuntimeError("Le modèle n'est pas encore entraîné.")
        padded = self.encode([text], max_len)
        pred = self.model.predict(padded, verbose=0)  # type: ignore[attr-defined]
        predicted_idx = int(np.argmax(pred))
        return self.responses[predicted_idx] if self.responses else str(predicted_idx)
