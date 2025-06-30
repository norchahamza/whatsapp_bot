import json
import csv
import os

CSV_PATH = "app/utils/intents.csv"
RESPONSES_PATH = ".vscode/response.json"

# Charger responses.json
with open(RESPONSES_PATH, encoding="utf-8") as f:
    responses = json.load(f)

# Extraire intentions depuis intents.csv
csv_intents = set()
with open(CSV_PATH, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        intent = row.get("intent", "").strip()
        if intent:
            csv_intents.add(intent)

# Ajouter les intentions manquantes dans responses.json
added_count = 0
for intent in sorted(csv_intents):
    if intent not in responses:
        responses[intent] = {
            "fr": "",
            "darija": "",
            "en": "",
            "ar": ""
        }
        added_count += 1

# Sauvegarder le fichier enrichi
with open(RESPONSES_PATH, "w", encoding="utf-8") as f:
    json.dump(responses, f, ensure_ascii=False, indent=2)

print(f"✅ responses.json enrichi avec {added_count} nouvelles intentions.")
