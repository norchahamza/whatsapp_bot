# scripts/clean_dataset.py
import pandas as pd
from pathlib import Path

# 📍 Fichier d'entrée unique (déjà fusionné et équilibré)
input_csv = Path("data/final_dataset_balanced.csv")
output_csv = Path("data/conversation_dataset_cleaned.csv")

# ⚠️ Intents à exclure (non utiles à l'entraînement)
excluded_intents = [
    'suggest', 'suggestion', 'suggest_close',
    'no_product', 'no_match', 'unrecognized',
    'suggestion_or_none', 'fallback_suggestion', 'empty_message'
]

# ⚠️ Messages bruyants à supprimer manuellement
excluded_messages = [
    'nawflis', 'pizze ma.', 'brise pisaillement',
    'p overlap', 'ok je orange mon müsse-flics'
]

# 📥 Chargement du dataset fusionné
df = pd.read_csv(input_csv)

# 🧹 Nettoyage
df = df[df["message"].notnull() & df["response"].notnull()]
df = df[~df["intent"].isin(excluded_intents)]
df = df[~df["message"].str.lower().isin([m.lower() for m in excluded_messages])]

# 🧽 Retirer les doublons exacts
df = df.drop_duplicates(subset=["message", "response"])

# 💾 Export final
df.to_csv(output_csv, index=False, encoding="utf-8")
print(f"✅ Dataset nettoyé sauvegardé dans : {output_csv}")
print(f"📊 Total de lignes conservées : {len(df)}")
# ===============================
# ➕ Fusion avec les intents augmentés
# ===============================
augmented_path = Path("data/intents.csv")
final_output_path = Path("data/training_data_final.csv")

if augmented_path.exists():
    print(f"📥 Fusion avec {augmented_path.name} ...")
    df_aug = pd.read_csv(augmented_path)

    # Ajout des colonnes manquantes pour uniformiser le format
    df_aug["datetime"] = ""
    df_aug["user_id"] = "synthetic"
    df_aug["response"] = ""  # vide pour génération automatique plus tard
    df_aug["lang"] = df_aug["text"].apply(lambda x: "darija" if any(c in x for c in "ءاأإبجحخدذرزسشصضطظعغفقكلمنهوي") else "fr")

    # Réorganiser les colonnes
    df_aug = df_aug[["datetime", "user_id", "text", "response", "intent", "lang"]]
    df_aug = df_aug.rename(columns={"text": "message"})

    # Fusion avec le dataset nettoyé
    df_final = pd.concat([df, df_aug], ignore_index=True)
    df_final = df_final.drop_duplicates(subset=["message", "intent"])

    # Export final enrichi
    df_final.to_csv(final_output_path, index=False, encoding="utf-8")
    print(f"✅ Dataset final enrichi sauvegardé dans : {final_output_path}")
    print(f"📊 Total de lignes dans le dataset final : {len(df_final)}")
else:
    print("⚠️ Fichier d'intentions augmentées non trouvé. Aucune fusion effectuée.")
