from exponent_server_sdk import PushClient, PushMessage
from .models import UserDevice

expo_client = PushClient()

def send_push_notification(user, title, body, data=None):
    try:
        # Get user's device
        device = UserDevice.objects.filter(user=user, is_active=True).first()
        if not device:
            return False

        # Construct message
        message = PushMessage(
            to=device.expo_token,
            title=title,
            body=body,
            data=data or {}
        )

        # Send notification
        response = expo_client.send_push_messages([message])
        return response[0]['status'] == 'ok'
    except Exception as e:
        print(f"Error sending notification: {str(e)}")
        return False
