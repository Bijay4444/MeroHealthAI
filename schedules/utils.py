from fcm_django.models import FCMDevice

def send_medication_reminder(user, medication):
    try:
        devices = FCMDevice.objects.filter(user=user, active=True)
        
        notification_data = {
            'title': 'Medication Reminder',
            'body': f"Time to take {medication.name}",
            'data': {
                'medication_id': medication.id,
                'type': 'medication_reminder'
            }
        }

        # Send to all user devices
        result = devices.send_message(
            title=notification_data['title'],
            body=notification_data['body'],
            data=notification_data['data']
        )
        return result
    except Exception as e:
        print(f"Error sending notification: {str(e)}")
        return False
