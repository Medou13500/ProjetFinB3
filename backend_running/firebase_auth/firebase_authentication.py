import os
import firebase_admin
from firebase_admin import auth, credentials, initialize_app

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.db import IntegrityError
from decouple import config

# 🔁 Import du modèle local d'utilisateur Django
from core.models import FirebaseUserModel  # adapte si ton modèle est ailleurs


# 🔐 Classe représentant un utilisateur Firebase compatible avec Django
class FirebaseUser:
    def __init__(self, uid, email, name=None):
        self.uid = uid
        self.email = email
        self.name = name or ""
        self.is_authenticated = True  # Indispensable pour DRF

    def __str__(self):
        return f"FirebaseUser({self.email})"


# 🚀 Initialisation unique de Firebase avec le fichier de clé
if not firebase_admin._apps:
    cred_path = config("FIREBASE_CREDENTIAL_PATH", default=None)

    if cred_path and os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        initialize_app(cred)
        print("✅ Firebase initialisé")
    else:
        print("❌ Clé Firebase introuvable ou invalide.")


# 🔐 Authentification DRF basée sur les ID tokens Firebase
class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        id_token = request.META.get('HTTP_AUTHORIZATION')

        if not id_token:
            raise AuthenticationFailed('No token provided')

        if id_token.startswith('Bearer '):
            id_token = id_token[7:]

        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception as e:
            raise AuthenticationFailed(f'Invalid token: {e}')

        uid = decoded_token.get('uid')
        email = decoded_token.get('email')
        name = decoded_token.get('name')
        
        # 👇 Extraction de first_name, last_name, username depuis le name complet
        username = name.split()[0] if name else ''
        first_name = name.split()[0] if name else ''
        last_name = ' '.join(name.split()[1:]) if name and len(name.split()) > 1 else ''

        # 🔄 Créer ou récupérer l'utilisateur Django lié à Firebase UID
        try:
            user = FirebaseUserModel.objects.get(uid=uid)
        except FirebaseUserModel.DoesNotExist:
            try:
                user = FirebaseUserModel.objects.get(email=email)
            except FirebaseUserModel.DoesNotExist:
                try:
                    user = FirebaseUserModel.objects.create(
                        uid=uid,
                        email=email,
                        name=name,
                        username=username,
                        first_name=first_name,
                        last_name=last_name
                    )
                except IntegrityError as e:
                    raise AuthenticationFailed(f"Erreur lors de la création de l'utilisateur : {e}")

        return (user, None)
