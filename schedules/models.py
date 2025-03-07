from django.db import models
from medications.models import Schedule
from users.models import CustomUser
from fcm_django.models import FCMDevice

class UserDevice(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    expo_token = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_devices'

class Reminder(models.Model):
    REMINDER_STATUS = [
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled')
    ]
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    sent_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=REMINDER_STATUS, default='PENDING')
    retry_count = models.IntegerField(default=0)
    last_retry = models.DateTimeField(null=True, blank=True)
    notification_sent = models.BooleanField(default=False)
    class Meta:
        ordering = ['-sent_time']
        unique_together = ('schedule', 'sent_time')
    
    def __str__(self):
        return f"Reminder for {self.schedule} at {self.sent_time}"
    

class AdherenceRecord(models.Model):
    ADHERENCE_STATUS = [
        ('NOT_TAKEN', 'Not Taken'),
        ('TAKEN', 'Taken'),
        ('SKIPPED', 'Skipped'),
        ('DELAYED', 'Delayed')
    ]
    reminder = models.OneToOneField(Reminder, on_delete=models.CASCADE, unique=True)
    taken_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ADHERENCE_STATUS, default='NOT_TAKEN')

    def __str__(self):
        return f"AdherenceRecord for {self.reminder}"
    

