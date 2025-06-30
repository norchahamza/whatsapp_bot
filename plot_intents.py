import pandas as pd
import os
import matplotlib.pyplot as plt

# 📍 Chargement du dataset final équilibré
data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/final_dataset_balanced.csv'))
df = pd.read_csv(data_path)

# ✅ Vérification de la colonne 'intent'
if "intent" not in df.columns:
    raise ValueError("La colonne 'intent' est manquante dans le fichier CSV.")

# 📊 Comptage des classes
intent_counts = df["intent"].value_counts()

# 🎨 Affichage du graphique
plt.figure(figsize=(10, 6))
intent_counts.plot(kind='bar', edgecolor='black')
plt.title("Répartition des classes d'intention")
plt.xlabel("Intent")
plt.ylabel("Nombre d'exemples")
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
