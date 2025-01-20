from django.db import models
from medications.models import Schedule

class Reminder(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    sent_time = models.DateTimeField()
    status = models.CharField(max_length=20)

class AdherenceRecord(models.Model):
    reminder = models.OneToOneField(Reminder, on_delete=models.CASCADE)
    taken_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='Not Taken')