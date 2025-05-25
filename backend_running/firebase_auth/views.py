from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .firebase_authentication import FirebaseAuthentication

class HelloFirebaseUser(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": "Bienvenue, utilisateur Firebase !",
            "uid": request.user.uid,
            "email": request.user.email,
            "name": request.user.name
        })
