from rest_framework import serializers
from .models import RunningStat
from .models import Challenge

class RunningStatSerializer(serializers.ModelSerializer):
    calories_burned = serializers.SerializerMethodField()
    
    class Meta:
        model = RunningStat
        fields = '__all__'
        read_only_fields = ['user']

    def get_calories_burned(self, obj):
        poids = self.context.get("weight", 70)  # on pourra passer ça depuis la vue
        return round(obj.distance_km * poids * 1.036, 2)

class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = '__all__'
        read_only_fields = ['user_email']
