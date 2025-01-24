from django.db import models
from medications.models import Schedule
from users.models import CustomUser

class Reminder(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    sent_time = models.DateTimeField()
    status = models.CharField(max_length=20)
    
    def __str__(self):
        return f"Reminder for {self.schedule} at {self.sent_time}"
    

class AdherenceRecord(models.Model):
    reminder = models.OneToOneField(Reminder, on_delete=models.CASCADE)
    taken_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='Not Taken')

    def __str__(self):
        return f"AdherenceRecord for {self.reminder}"
    

