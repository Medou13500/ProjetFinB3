from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from core.models import FirebaseUserModel
import firebase_admin
from firebase_admin import auth, credentials, initialize_app
import os
from decouple import config
from django.db import IntegrityError


if not firebase_admin._apps:
    cred_path = config("FIREBASE_CREDENTIAL_PATH", default=None)
    if cred_path and os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        initialize_app(cred)
        print("✅ Firebase initialisé")
    else:
        print("❌ Clé Firebase introuvable ou invalide.")


class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        id_token = request.META.get('HTTP_AUTHORIZATION')

        if not id_token:
            return None  # Pas de token, on laisse DRF gérer l’absence

        if id_token.startswith('Bearer '):
            id_token = id_token[7:]

        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception as e:
            raise AuthenticationFailed(f'Token invalide: {e}')

        uid = decoded_token.get('uid')
        email = decoded_token.get('email')
        name = decoded_token.get('name', '')

        if not uid or not email:
            raise AuthenticationFailed('Token Firebase invalide : uid ou email manquant.')

        username = name.split()[0] if name else ''
        first_name = name.split()[0] if name else ''
        last_name = ' '.join(name.split()[1:]) if name and len(name.split()) > 1 else ''

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
                    raise AuthenticationFailed(f"Erreur création utilisateur : {e}")

        return (user, None)
