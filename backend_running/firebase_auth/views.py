from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .firebase_authentication import FirebaseAuthentication
from core.models import FirebaseUserModel

class ListFirebaseUsers(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = FirebaseUserModel.objects.all()
        return Response([
            {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name
            } for user in users
        ])

class HelloFirebaseUser(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retourne les informations de l'utilisateur authentifié via Firebase.",
        responses={
            200: openapi.Response(
                description="Informations Firebase de l'utilisateur",
                examples={
                    "application/json": {
                        "message": "Bienvenue, utilisateur Firebase !",
                        "uid": "firebase-uid-exemple",
                        "email": "user@example.com",
                        "name": "John Doe",
                        "username": "johndoe",
                        "first_name": "John",
                        "last_name": "Doe"
                    }
                }
            )
        }
    )
    def get(self, request):
        # On va chercher l'utilisateur dans la base FirebaseUserModel via son UID
        firebase_user = FirebaseUserModel.objects.filter(uid=request.user.uid).first()

        if firebase_user:
            return Response({
                "message": f"Bienvenue, {firebase_user.first_name or firebase_user.name or firebase_user.username} !",
                "uid": firebase_user.uid,
                "email": firebase_user.email,
                "name": firebase_user.name,
                "username": firebase_user.username,
                "first_name": firebase_user.first_name,
                "last_name": firebase_user.last_name
            })
        else:
            return Response({"error": "Utilisateur non trouvé dans la base de données."}, status=404)
