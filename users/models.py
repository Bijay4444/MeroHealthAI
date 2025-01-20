from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ])

class NotificationPreference(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=50)
    is_enabled = models.BooleanField(default=True)

class CaregiverRelationship(models.Model):
    user = models.ForeignKey(CustomUser, related_name='patient', on_delete=models.CASCADE)
    caregiver = models.ForeignKey(CustomUser, related_name='caregiver', on_delete=models.CASCADE)
    relationship = models.CharField(max_length=50)