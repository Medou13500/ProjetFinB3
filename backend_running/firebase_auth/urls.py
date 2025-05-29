from django.urls import path  # <-- include ne sert à rien ici
from .views import HelloFirebaseUser

urlpatterns = [
    path('me/', HelloFirebaseUser.as_view(), name='firebase-user'),
]
