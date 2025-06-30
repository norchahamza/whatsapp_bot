import pandas as pd
from sklearn.utils import resample

# Charger le dataset fusionné
df = pd.read_csv("data/final_dataset.csv")

# Compter les occurrences par classe
counts = df["intent"].value_counts()
print("📊 Répartition avant équilibrage :")
print(counts)

# Trouver la taille de la classe minoritaire
min_samples = counts.min()

# Rééchantillonnage (downsampling ou upsampling)
balanced_df = pd.DataFrame()
for label in counts.index:
    subset = df[df["intent"] == label]
    if len(subset) > min_samples:
        subset_balanced = resample(subset, replace=False, n_samples=min_samples, random_state=42)
    else:
        subset_balanced = resample(subset, replace=True, n_samples=min_samples, random_state=42)
    balanced_df = pd.concat([balanced_df, subset_balanced])

# Mélanger et sauvegarder
balanced_df = balanced_df.sample(frac=1, random_state=42)
balanced_df.to_csv("data/final_dataset_balanced.csv", index=False, encoding="utf-8-sig")
print("✅ Dataset équilibré sauvegardé dans : data/final_dataset_balanced.csv")
