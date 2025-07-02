from django.db import models
from core.models import FirebaseUserModel
from django.utils import timezone
from django.contrib.auth import get_user_model


class RunningStat(models.Model):
    user = models.ForeignKey(FirebaseUserModel, on_delete=models.CASCADE)
    distance_km = models.FloatField()
    duration_minutes = models.FloatField()
    run_type = models.CharField(max_length=50, default='training')
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(default=timezone.now)
    note = models.TextField(blank=True, null=True)
    calories = models.IntegerField(null=True, blank=True)
    heart_rate_avg = models.IntegerField(null=True, blank=True)




    def __str__(self):
        return f"{self.user.email} - {self.distance_km} km en {self.duration_minutes} min"
    
class Challenge(models.Model):
    user_email = models.EmailField(null=True, blank=True)
    title = models.CharField(max_length=100)
    target_distance_km = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
     return f"{self.title} - {self.user_email}"

