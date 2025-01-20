from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ])
    
    def __str__(self):
        return self.email

class NotificationPreference(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=50)
    is_enabled = models.BooleanField(default=True)

class CaregiverRelationship(models.Model):
    user = models.ForeignKey(CustomUser, related_name='patient', on_delete=models.CASCADE)
    caregiver = models.ForeignKey(CustomUser, related_name='caregiver', on_delete=models.CASCADE)
    relationship = models.CharField(max_length=50)
    
    class Meta:
        unique_together = ('user', 'caregiver')