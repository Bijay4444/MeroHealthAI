from .services import send_push_notification
from celery import shared_task
from django.utils import timezone
from .models import Schedule, Reminder
from datetime import timedelta
from medications.models import Schedule
from .models import Reminder


@shared_task
def send_medication_reminder(reminder_id):
    try:
        reminder = Reminder.objects.get(id=reminder_id)
        user = reminder.schedule.user
        medication_name = reminder.schedule.medication.name
        
        success = send_push_notification(
            user=user,
            title="Medication Reminder",
            body=f"Time to take {medication_name}",
            data={
                'reminder_id': reminder.id,
                'medication_id': reminder.schedule.medication.id
            }
        )
        
        reminder.notification_sent = success
        reminder.status = 'SENT' if success else 'FAILED'
        reminder.save()
        
        return success
    except Reminder.DoesNotExist:
        return False
    
@shared_task
def generate_daily_reminders():
    """Daily task to generate reminders for all active schedules."""
    active_schedules = Schedule.objects.filter(is_active=True)
    
    # Filter out expired schedules
    now = timezone.now()
    active_schedules = active_schedules.filter(
        models.Q(expires_at__gt=now) | models.Q(expires_at__isnull=True)
    )
    
    for schedule in active_schedules:
        schedule.generate_reminders()
    
    return f"Generated reminders for {active_schedules.count()} active schedules"

@shared_task
def check_upcoming_reminders():
    """Task to check for upcoming reminders and schedule notifications."""
    now = timezone.now()
    upcoming_time = now + timedelta(minutes=30)
    
    # Find reminders that are coming up in the next 30 minutes
    upcoming_reminders = Reminder.objects.filter(
        sent_time__gte=now,
        sent_time__lte=upcoming_time,
        status='PENDING',
        notification_sent=False
    )
    
    for reminder in upcoming_reminders:
        # Schedule the notification task to be sent at the reminder time
        send_medication_reminder.apply_async(
            args=[reminder.id],
            eta=reminder.sent_time
        )
    
    return f"Scheduled notifications for {upcoming_reminders.count()} upcoming reminders"

@shared_task
def clean_old_reminders():
    """Task to clean up old reminders that are no longer needed."""
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    # Delete old reminders that have been processed
    old_reminders = Reminder.objects.filter(
        sent_time__lt=thirty_days_ago,
        status__in=['SENT', 'FAILED', 'CANCELLED']
    )
    
    count = old_reminders.count()
    old_reminders.delete()
    
    return f"Cleaned up {count} old reminders"