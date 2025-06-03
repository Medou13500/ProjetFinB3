from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class FirebaseUserManager(BaseUserManager):
    def create_user(self, uid, email=None, name=None):
        user = self.model(uid=uid, email=email, name=name)
        user.set_unusable_password()  # car on n'utilise pas Django pour l'auth
        user.save(using=self._db)
        return user

class FirebaseUserModel(AbstractBaseUser):
    uid = models.CharField(max_length=128, unique=True)  # UID Firebase
    email = models.EmailField(blank=True, null=True, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)

    objects = FirebaseUserManager()

    USERNAME_FIELD = 'uid'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email or self.uid
