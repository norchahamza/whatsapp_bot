#app\ml\create_dataset.py
import csv
import os
from datetime import datetime

# Dossier de sortie
output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data")
os.makedirs(output_dir, exist_ok=True)

# Chemin complet du fichier CSV
csv_path = os.path.join(output_dir, "conversation_dataset.csv")

# Création du fichier avec les en-têtes
headers = ["timestamp", "user_id", "message", "response", "intent"]

with open(csv_path, mode="w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(headers)

print(f"✅ Fichier CSV créé à : {csv_path}")
