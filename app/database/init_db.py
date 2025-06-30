# app/database/init_db.py
import sqlite3
import os

def create_database():
    DB_PATH = os.path.join(os.path.dirname(__file__), "products.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL UNIQUE,
        tailles_disponibles TEXT,
        quantite INTEGER,
        type TEXT CHECK(type IN ('physique', 'digital')) NOT NULL DEFAULT 'physique',
        duree TEXT,  -- pour produits digitaux, ex: "30 jours"
        image_path TEXT
    )
    ''')

    # Liste de produits exemple
    produits = [
        ("pyjama bleu", "S,M,L", 10, "physique", None, "images/pyjama1.jpg"),
        ("robe rouge", "M,L", 5, "physique", None, "images/robe1.jpg"),
        ("abonnement netflix", None, 9999, "digital", "30 jours", None),
        ("licence office", None, 9999, "digital", "1 an", None)
    ]

    cursor.executemany('''
    INSERT OR IGNORE INTO produits (nom, tailles_disponibles, quantite, type, duree, image_path)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', produits)

    conn.commit()
    conn.close()
    print("✅ Base de données initialisée avec succès.")

if __name__ == "__main__":
    create_database()
