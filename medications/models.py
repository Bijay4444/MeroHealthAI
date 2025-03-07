from django.db import models
from users.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime, timedelta

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
    
    @property 
    def time_iso(self):
        return self.time.isoformat() if self.time else None
    
    def __str__(self):
        return f"{self.user.name} - {self.medication.name} at {self.time}"
    
    def generate_reminders(self, days_ahead=1):  # Changed from 30 to 1
        """Generate reminders for this schedule based on frequency."""
        from schedules.models import Reminder
        
        today = timezone.now().date()
        end_date = today + timedelta(days=days_ahead)
        
        # Clear any future pending reminders for this schedule
        Reminder.objects.filter(
            schedule=self,
            sent_time__date__gte=today,
            status='PENDING'
        ).delete()
        
        current_date = today
        while current_date <= end_date:
            #use the time as entered by user without timezone
            local_time = datetime.combine(current_date, self.time)
            
            #convert to UTC for storing in the database
            reminder_time = timezone.make_aware(local_time)
            
            # Check if a reminder already exists for this schedule and time
            existing_reminder = Reminder.objects.filter(
                schedule=self,
                sent_time__date=current_date,
            ).exists()
            
            if existing_reminder:
                # Skip creating a duplicate reminder
                current_date += timedelta(days=1)
                continue
                
            # For DAILY frequency - create for every day
            if self.frequency == 'DAILY':
                Reminder.objects.get_or_create(
                    schedule=self,
                    sent_time=reminder_time,
                    status='PENDING'
                )
            
            # For WEEKLY frequency - only create if it's the same day of week
            elif self.frequency == 'WEEKLY' and current_date.weekday() == today.weekday():
                Reminder.objects.get_or_create(
                    schedule=self,
                    sent_time=reminder_time,
                    status='PENDING'
                )
            
            # For MONTHLY frequency - only create if it's the same day of month
            elif self.frequency == 'MONTHLY' and current_date.day == today.day:
                Reminder.objects.get_or_create(
                    schedule=self,
                    sent_time=reminder_time,
                    status='PENDING'
                )
            
            # No reminders for AS_NEEDED frequency
            
            current_date += timedelta(days=1)

# a signal to automatically generate reminders when a schedule is created or updated
@receiver(post_save, sender=Schedule)
def schedule_post_save(sender, instance, created, **kwargs):
    instance.generate_reminders()
