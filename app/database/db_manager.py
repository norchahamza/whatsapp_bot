# app/database/db_manager.py

import sqlite3
import os
import difflib

DB_PATH = os.path.join(os.path.dirname(__file__), "products.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def find_product_by_name(nom):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM produits WHERE LOWER(nom) LIKE ?", 
                ('%' + nom.lower() + '%',)
            )
            return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"❌ Erreur SQL dans find_product_by_name : {e}")
        return None

def get_all_products():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM produits")
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"❌ Erreur SQL dans get_all_products : {e}")
        return []

def suggest_similar_product(nom_proche):
    produits = get_all_products()
    noms = [p[1] for p in produits]  # p[1] = nom du produit
    match = difflib.get_close_matches(nom_proche.lower(), noms, n=1, cutoff=0.6)
    if match:
        return find_product_by_name(match[0])
    return None

def update_product_quantity(nom, new_quantity):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE produits SET stock = ? WHERE LOWER(nom) = LOWER(?)", 
                (new_quantity, nom)
            )
            conn.commit()
    except sqlite3.Error as e:
        print(f"❌ Erreur SQL dans update_product_quantity : {e}")
        return False
    return True