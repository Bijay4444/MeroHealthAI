from celery import shared_task
from django.utils import timezone
from .models import Schedule, Reminder
from datetime import timedelta

# schedules/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import Schedule, Reminder
from datetime import timedelta

@shared_task
def send_reminders():
    current_time = timezone.now()
    pending_reminders = Reminder.objects.filter(
        status='PENDING',
        sent_time__lte=current_time
    )
    
    for reminder in pending_reminders:
        # Send push notification
        success = send_medication_reminder(
            reminder.schedule.user,
            reminder.schedule.medication
        )
        
        if success:
            reminder.status = 'SENT'
            reminder.save()


@shared_task
def generate_reminders():
    current_time = timezone.now()
    schedules = Schedule.objects.filter(
        is_active=True,
        expires_at__gt=current_time
    )
    
    for schedule in schedules:
        # Create reminder based on frequency
        if schedule.frequency == 'DAILY':
            next_reminder_time = current_time + timedelta(days=1)
        elif schedule.frequency == 'WEEKLY':
            next_reminder_time = current_time + timedelta(weeks=1)
            
        Reminder.objects.create(
            schedule=schedule,
            sent_time=next_reminder_time,
            status='PENDING'
        )

@shared_task
def send_reminders():
    current_time = timezone.now()
    pending_reminders = Reminder.objects.filter(
        status='PENDING',
        sent_time__lte=current_time
    )
    
    for reminder in pending_reminders:
        # Send notification based on user preferences
        user_preferences = reminder.schedule.user.notification_preferences
        if user_preferences.email:
            send_email_notification(reminder)
        if user_preferences.sms:
            send_sms_notification(reminder)
        
        reminder.status = 'SENT'
        reminder.save()
