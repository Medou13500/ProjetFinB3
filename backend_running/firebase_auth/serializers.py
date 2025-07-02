from rest_framework import serializers
from core.models import FirebaseUserModel

class FirebaseUserSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(allow_blank=True, default="")  # 👈 important
    first_name = serializers.CharField(allow_blank=True, default="")
    name = serializers.CharField(allow_blank=True, default="")
    username = serializers.CharField(allow_blank=True, default="")

    class Meta:
        model = FirebaseUserModel
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'name']
