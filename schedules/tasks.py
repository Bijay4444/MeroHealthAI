from .services import send_push_notification
from celery import shared_task
from django.utils import timezone
from .models import Reminder
from datetime import timedelta
from medications.models import Schedule
import pytz

@shared_task
def send_medication_reminder(reminder_id):
    """
    Send a push notification for a specific medication reminder.
    Updates the reminder status after sending.
    """
    try:
        reminder = Reminder.objects.get(id=reminder_id)
        user = reminder.schedule.user
        medication_name = reminder.schedule.medication.name
        
        print(f"Sending notification for reminder {reminder_id}: {medication_name}")
        
        success = send_push_notification(
            user=user,
            title="Medication Reminder",
            body=f"Time to take {medication_name}",
            data={
                'reminder_id': reminder.id,
                'medication_id': reminder.schedule.medication.id
            }
        )
        
        # Update reminder status regardless of success to prevent repeated notifications
        reminder.notification_sent = True
        reminder.status = 'SENT' if success else 'FAILED'
        reminder.save()
        
        return success
    except Reminder.DoesNotExist:
        return False

@shared_task
def check_upcoming_reminders():
    """
    Check for upcoming reminders and schedule notifications.
    Properly handles timezone conversion between UTC and Nepal time.
    """
    # Get current time in UTC (Django's timezone.now() returns UTC)
    now_utc = timezone.now()
    
    # Define the Nepal timezone
    nepal_tz = pytz.timezone('Asia/Kathmandu')
    
    # Convert current UTC time to Nepal time for logging
    now_nepal = now_utc.astimezone(nepal_tz)
    
    # Look 15 minutes ahead for upcoming reminders
    upcoming_time_utc = now_utc + timedelta(minutes=15)
    
    # Also check 5 minutes in the past to catch any missed reminders
    past_time_utc = now_utc - timedelta(minutes=5)
    
    print(f"Current time (Nepal): {now_nepal}, checking for reminders between {past_time_utc} and {upcoming_time_utc}")
    
    # Query reminders in UTC time range
    upcoming_reminders = Reminder.objects.filter(
        sent_time__gte=past_time_utc,
        sent_time__lte=upcoming_time_utc,
        status='PENDING',
        notification_sent=False
    )
    
    print(f"Found {upcoming_reminders.count()} upcoming reminders")
    
    for reminder in upcoming_reminders:
        # Convert reminder time to Nepal time for logging
        reminder_time_nepal = reminder.sent_time.astimezone(nepal_tz)
        print(f"Scheduling notification for reminder {reminder.id} at {reminder_time_nepal} (Nepal time)")
        
        # Send notification immediately for past reminders
        if reminder.sent_time <= now_utc:
            send_medication_reminder.delay(reminder.id)
        else:
            # Schedule notification at the exact reminder time
            send_medication_reminder.apply_async(
                args=[reminder.id],
                eta=reminder.sent_time
            )
        
        # Mark reminder as having notification scheduled
        reminder.notification_sent = True
        reminder.save()
    
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
