import os
from firebase_admin import credentials, initialize_app
from .firebase_init import *  # déclenche l'init Firebase automatiquement

FIREBASE_KEY_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'serviceAccountKey.json'
)

print(f"🔍 Tentative de chargement de la clé : {FIREBASE_KEY_PATH}")

try:
    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    initialize_app(cred)
    print("✅ Firebase initialisé")
except Exception as e:
    print("❌ Clé Firebase introuvable ou invalide.")
    print(str(e))
