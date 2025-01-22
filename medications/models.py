from django.db import models
from users.models import CustomUser

class Medication(models.Model):
    name = models.CharField(max_length=100)
    instructions = models.TextField()
    
    def __str__(self):
        return self.name
    

class Schedule(models.Model):
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=50)
    time = models.TimeField()
    frequency = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.name} - {self.medication.name} at {self.time}"