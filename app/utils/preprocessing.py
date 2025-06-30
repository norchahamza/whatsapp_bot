import re

# === Dictionnaire de normalisation Darija → Français ===
REPLACEMENTS = {
    # 🟢 Salutations
    "salam": "bonjour", "slm": "bonjour", "salaam": "bonjour",
    "salamou": "bonjour", "salut": "bonjour", "slm3lykom": "bonjour",
    "salam alikoum": "bonjour",

    # 🟢 Demande
    "bgha": "je veux", "brit": "je veux", "bghit": "je veux", "brise": "je veux", "brich": "je veux",
    "britch": "je veux", "nabghi": "je veux", "bigha": "je veux", "nbghi": "je veux",
    "nchri": "je veux", "achri": "je veux", "nabgha": "je veux",

    # 🟢 Produits
    "nawflis": "netflix", "netflis": "netflix", "netfliks": "netflix", "naitflix": "netflix", "neflik": "netflix",
    "bijama": "pyjama", "pijama": "pyjama", "bijema": "pyjama", "pyjamas": "pyjama",
    "bijham": "pyjama", "pyzama": "pyjama", "bijam": "pyjama", "bijamat": "pyjama",
    "kask": "casque", "kassk": "casque", "caske": "casque", "kaskette": "casque",
    "roj": "robe", "rwb": "robe", "rub": "robe", "hob": "robe", "rop": "robe",

    # 🟢 Tailles
    "kbir": "taille L", "sghir": "taille S", "moyen": "taille M", "standard": "taille M",
    "m": "taille M", "s": "taille S", "l": "taille L",
    "xl": "taille XL", "xxl": "taille XXL", "xs": "taille XS", "xxxl": "taille XXXL",

    # 🟢 Couleurs
    "k7al": "noir", "ke7al": "noir", "khal": "noir", "kahal": "noir",
    "byad": "blanc", "abyad": "blanc", "zraq": "bleu", "hmr": "rouge",

    # 🟢 Autres
    "ma3aya": "avec moi", "m3aya": "avec moi", "smiyti": "je m'appelle",
    "choukran": "merci", "chokran": "merci", "shukran": "merci", "merci": "merci",
    "hna": "ici", "ma3ndich": "je n’ai pas", "ndi": "j’ai", "andi": "j’ai"
}


def normaliser_darija(text: str, debug: bool = False) -> str:
    """
    Remplace les mots Darija par leurs équivalents français, mot à mot.
    """
    text = text.lower()
    mots = re.findall(r'\w+', text)
    mots_norm = []

    for mot in mots:
        mot_remplace = REPLACEMENTS.get(mot, mot)
        if debug and mot != mot_remplace:
            print(f"🔁 Remplacé: '{mot}' → '{mot_remplace}'")
        mots_norm.append(mot_remplace)

    return " ".join(mots_norm)


def clean_text(text: str) -> str:
    """
    Nettoie le texte : supprime les caractères spéciaux, accents, ponctuation, etc.
    """
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9éèàùâêîôûç ]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
