from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    USER_TYPES = [
        ('PATIENT', 'Patient'),
        ('CAREGIVER', 'Caregiver'),
    ]
    
    username = None
    email = models.EmailField(_("email address"), unique=True)
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPES,
        default='PATIENT'
    )
    
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
    NOTIFICATION_TYPES = [
        ('EMAIL', 'Email'),
        ('SMS', 'SMS'),
        ('PUSH', 'Push Notification')
    ]
    
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE,
        related_name='notification_preferences'
    )
    notification_methods = models.JSONField(
        default=dict,
        help_text='Stores notification preferences as a JSON object'
    )
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)
    is_enabled = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Notification Preference'
        verbose_name_plural = 'Notification Preferences'
    
    def __str__(self):
        return f"Notification settings for {self.user.email}"
    
    def save(self, *args, **kwargs):
        if not self.notification_methods:
            self.notification_methods = {
                'EMAIL': False,
                'SMS': False,
                'PUSH': True
            }
        super().save(*args, **kwargs)


class CaregiverRelationship(models.Model):
    RELATIONSHIP_TYPES = [
        ('FAMILY', 'Family Member'),
        ('DOCTOR', 'Doctor'),
        ('NURSE', 'Nurse'),
        ('CARETAKER', 'Professional Caretaker'),
        ('OTHER', 'Other')
    ]
    
    PERMISSION_LEVELS = [
        ('VIEW', 'View Only'),
        ('MANAGE', 'Manage Medications'),
        ('FULL', 'Full Access')
    ]
    
    user = models.ForeignKey(
        CustomUser, 
        related_name='patient_relationships',
        on_delete=models.CASCADE
    )
    caregiver = models.ForeignKey(
        CustomUser,
        related_name='caregiver_relationships',
        on_delete=models.CASCADE
    )
    relationship = models.CharField(
        max_length=50,
        choices=RELATIONSHIP_TYPES,
        default='OTHER'
    )
    permission_level = models.CharField(
        max_length=20,
        choices=PERMISSION_LEVELS,
        default='VIEW'
    )
    can_view_adherence = models.BooleanField(default=True)
    can_modify_schedule = models.BooleanField(default=False)
    emergency_contact = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('user', 'caregiver')
        ordering = ['-date_added']
    
    def __str__(self):
        return f"{self.caregiver.name} -> {self.user.name} ({self.get_relationship_display()})"
    
    def save(self, *args, **kwargs):
        if self.permission_level == 'FULL':
            self.can_view_adherence = True
            self.can_modify_schedule = True
        elif self.permission_level == 'MANAGE':
            self.can_view_adherence = True
            self.can_modify_schedule = True
        super().save(*args, **kwargs)
