from app.config import Config
import os

print("Chemin vers le fichier :", Config.RESPONSES_FILE)

if os.path.exists(Config.RESPONSES_FILE):
    print("✅ Le fichier response.json est accessible.")
else:
    print("❌ Le fichier response.json est introuvable.")
#merge_datasets.py