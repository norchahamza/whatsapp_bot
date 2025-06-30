import pandas as pd
import os

# Fichiers
INTENTS_CSV = "app/utils/intents.csv"
DATASETS = [
    "data/final_dataset.csv",
    "data/final_dataset_balanced.csv"
]

def load_dataset(paths):
    dfs = []
    for path in paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            dfs.append(df)
        else:
            print(f"❌ Fichier introuvable : {path}")
    return pd.concat(dfs, ignore_index=True)

def clean_dataset(df):
    df = df.dropna(subset=["message", "intent", "lang"])
    df["message"] = df["message"].str.strip().str.lower()
    df["intent"] = df["intent"].str.strip().str.lower()
    df["lang"] = df["lang"].str.strip().str.lower()
    df["source"] = "auto_augmented"
    df = df.drop_duplicates(subset=["message", "intent", "lang"])
    return df[["message", "intent", "lang", "source"]]

def enrich_intents():
    # Chargement existant
    if os.path.exists(INTENTS_CSV):
        existing = pd.read_csv(INTENTS_CSV)
        existing["message"] = existing["message"].str.strip().str.lower()
        existing["intent"] = existing["intent"].str.strip().str.lower()
        existing["lang"] = existing["lang"].str.strip().str.lower()
    else:
        print("⚠️ Aucun fichier intents.csv trouvé, création d’un nouveau.")
        existing = pd.DataFrame(columns=["message", "intent", "lang", "source"])

    # Chargement & nettoyage des datasets
    raw_data = load_dataset(DATASETS)
    cleaned_data = clean_dataset(raw_data)

    # Fusion intelligente
    combined = pd.concat([existing, cleaned_data], ignore_index=True)
    combined = combined.drop_duplicates(subset=["message", "intent", "lang"])

    # Sauvegarde
    combined.to_csv(INTENTS_CSV, index=False, encoding="utf-8")
    print(f"✅ intents.csv mis à jour avec {len(combined) - len(existing)} nouvelles phrases.")
    print(f"📁 Total actuel : {len(combined)} entrées dans app/utils/intents.csv")

if __name__ == "__main__":
    enrich_intents()
