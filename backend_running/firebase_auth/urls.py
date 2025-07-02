from django.urls import path  # <-- include ne sert à rien ici
from firebase_auth.views import  HelloFirebaseUser,ListFirebaseUsers


urlpatterns = [
    path('me/', HelloFirebaseUser.as_view(), name='firebase-user'),
    path('all/', ListFirebaseUsers.as_view(), name='list-firebase-users'),
]