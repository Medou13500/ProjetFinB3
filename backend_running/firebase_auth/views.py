from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .firebase_authentication import FirebaseAuthentication

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
                        "name": "John Doe"
                    }
                }
            )
        }
    )
    def get(self, request):
        return Response({
            "message": "Bienvenue, utilisateur Firebase !",
            "uid": request.user.uid,
            "email": request.user.email,
            "name": request.user.name
        })
