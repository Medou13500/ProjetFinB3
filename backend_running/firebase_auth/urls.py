from django.urls import path
from .views import HelloFirebaseUser

urlpatterns = [
    path('me/', HelloFirebaseUser.as_view(), name='firebase-user'),
]
