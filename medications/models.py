from django.db import models
from users.models import CustomUser

class Medication(models.Model):
    FREQUENCY_CHOICES = [
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('AS_NEEDED', 'As Needed')
    ]
    name = models.CharField(max_length=100)
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    

class Schedule(models.Model):
    TIMING_CHOICES = [
        ('BEFORE_MEAL', 'Before Meal'),
        ('AFTER_MEAL', 'After Meal'),
        ('WITH_MEAL', 'With Meal'),
        ('ANY_TIME', 'Any Time')
    ]
    
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=50)
    time = models.TimeField()
    frequency = models.CharField(max_length=50, choices=Medication.FREQUENCY_CHOICES)
    timing = models.CharField(max_length=50, choices=TIMING_CHOICES, default='ANY_TIME')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.name} - {self.medication.name} at {self.time}"