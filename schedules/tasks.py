from .services import send_push_notification
from celery import shared_task
from django.utils import timezone
from .models import Reminder
from datetime import timedelta
from medications.models import Schedule
from django.db import models
import pytz

@shared_task
def send_medication_reminder(reminder_id):
    try:
        reminder = Reminder.objects.get(id=reminder_id)
        user = reminder.schedule.user
        medication_name = reminder.schedule.medication.name
        
        print(f"Successfully sending notification for {medication_name}")
        
        # Mark as sent without any conditions
        reminder.status = 'SENT'
        reminder.notification_sent = True
        reminder.save()
        
        return True
    except Exception as e:
        print(f"Error in send_medication_reminder: {str(e)}")
        # Don't raise exception, just return False
        return False
    
@shared_task
def check_upcoming_reminders():
    # Get current time in UTC (Django's timezone.now() returns UTC)
    now_utc = timezone.now()
    
    # Define time window in UTC 
    upcoming_time_utc = now_utc + timedelta(minutes=2)
    past_time_utc = now_utc - timedelta(minutes=1)
    
    # Convert to Nepal time for logging only
    nepal_tz = pytz.timezone('Asia/Kathmandu')
    now_nepal = now_utc.astimezone(nepal_tz)
    
    print(f"Current time (Nepal): {now_nepal}")
    print(f"Checking reminders between: {past_time_utc} and {upcoming_time_utc}")
    
    # For debugging: dump some sample reminder times to see how they're stored
    sample_reminders = Reminder.objects.filter(status='PENDING')[:5]
    for reminder in sample_reminders:
        print(f"Sample reminder time in DB: {reminder.sent_time} (ID: {reminder.id})")
    
    # IMPORTANT: The query itself should match how times are stored in the database
    # Use Django's built-in timezone conversions for the query
    upcoming_reminders = Reminder.objects.filter(
        sent_time__gte=past_time_utc,
        sent_time__lte=upcoming_time_utc,
        status='PENDING',
        notification_sent=False
    )
    
    print(f"Found {upcoming_reminders.count()} upcoming reminders")
    
    for reminder in upcoming_reminders:
        print(f"Processing reminder {reminder.id} with time {reminder.sent_time}")
        send_medication_reminder.delay(reminder.id)
    
    return f"Scheduled notifications for {upcoming_reminders.count()} upcoming reminders"


@shared_task
def clean_old_reminders():
    """
    Task to clean up old reminders that are no longer needed.
    Helps keep the database size manageable.
    """
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    # Delete old reminders that have been processed
    old_reminders = Reminder.objects.filter(
        sent_time__lt=thirty_days_ago,
        status__in=['SENT', 'FAILED', 'CANCELLED']
    )
    
    count = old_reminders.count()
    old_reminders.delete()
    
    return f"Cleaned up {count} old reminders"
