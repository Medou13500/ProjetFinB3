from rest_framework import serializers
from .models import RunningStat, Challenge

class RunningStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunningStat
        fields = '__all__'

class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = '__all__'
