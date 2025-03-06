from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Reminder, AdherenceRecord, UserDevice
from users.models import NotificationPreference
from users.serializers import NotificationPreferenceSerializer
from .serializers import ReminderSerializer, AdherenceRecordSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
# from fcm_django.models import FCMDevice
from exponent_server_sdk import PushClient, PushMessage
from datetime import timedelta
from django.db.models import F
from rest_framework.views import APIView

expo_client = PushClient()
class ReminderListCreateView(generics.ListCreateAPIView):
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Reminder.objects.filter(
            schedule__user=user
        ).select_related('schedule', 'schedule__medication')
    
    @action(detail=False, methods=['GET'])
    def today(self, request):
        today = timezone.now().date()
        reminders = self.get_queryset().filter(sent_time__date=today)
        serializer = self.get_serializer(reminders, many=True)
        return Response(serializer.data)

class ReminderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated]

#for reminders and adherence records     
@api_view(['GET'])
def upcoming_reminders(request):
    reminders = Reminder.objects.filter(
        schedule__user=request.user,
        sent_time__gte=timezone.now()
    ).order_by('sent_time')
    serializer = ReminderSerializer(reminders, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def mark_reminder_taken(request, pk):
    try:
        reminder = Reminder.objects.get(pk=pk, schedule__user=request.user)
        # Get or create adherence record
        adherence_record, created = AdherenceRecord.objects.get_or_create(
            reminder=reminder,
            defaults={
                'taken_time': timezone.now(),
                'status': 'TAKEN'
            }
        )
        
        # If record exists, update it
        if not created:
            adherence_record.taken_time = timezone.now()
            adherence_record.status = 'TAKEN'
            adherence_record.save()
            
        return Response(status=status.HTTP_200_OK)
    except Reminder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class AdherenceRecordListCreateView(generics.ListCreateAPIView):
    serializer_class = AdherenceRecordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return AdherenceRecord.objects.filter(
            reminder__schedule__user=user
        ).select_related('reminder', 'reminder__schedule')
    
    def perform_create(self, serializer):
        reminder = serializer.validated_data['reminder']
        if reminder.schedule.user != self.request.user:
            raise PermissionDenied("Not authorized to create adherence record")
        serializer.save()

class AdherenceRecordRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdherenceRecord.objects.all()
    serializer_class = AdherenceRecordSerializer
    permission_classes = [IsAuthenticated]

class NotificationPreferenceDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj, created = NotificationPreference.objects.get_or_create(user=self.request.user)
        return obj

################# AdherenceRecord Scoring Algorithm ##########################
class MedicationAdherenceScoreView(APIView):
    permission_classes = [IsAuthenticated]

    def calculate_adherence_score(self, user_id, time_period=30):
        """
        Calculate medication adherence score using a weighted algorithm
        - Taken on time (within 30 mins): full weight (1.0)
        - Taken late (after 30 mins): half weight (0.5)
        - Skipped/Not taken: zero weight (0.0)
        """
        end_date = timezone.now()
        start_date = end_date - timedelta(days=time_period)
        
        # Get all reminders for the user in the time period
        reminders = Reminder.objects.filter(
            schedule__user_id=user_id,
            sent_time__gte=start_date,
            sent_time__lte=end_date
        )
        
        total_reminders = reminders.count()
        if total_reminders == 0:
            return 100
            
        # Count reminders taken on time (within 30 minutes)
        taken_on_time = AdherenceRecord.objects.filter(
            reminder__in=reminders,
            status='TAKEN',
            taken_time__lte=F('reminder__sent_time') + timedelta(minutes=30)
        ).count()
        
        # Count reminders taken late (after 30 minutes)
        taken_late = AdherenceRecord.objects.filter(
            reminder__in=reminders,
            status='TAKEN',
            taken_time__gt=F('reminder__sent_time') + timedelta(minutes=30)
        ).count()
        
        # Calculate weighted score
        score = ((taken_on_time + (0.5 * taken_late)) / total_reminders) * 100
        return round(score, 2)

    def get(self, request):
        score = self.calculate_adherence_score(request.user.id)
        return Response({
            'adherence_score': score,
            'user': request.user.id,
            'message': self.get_adherence_message(score)
        })
    
    def get_adherence_message(self, score):
        if score >= 90:
            return "Excellent medication adherence!"
        elif score >= 80:
            return "Good adherence, but there's room for improvement."
        elif score >= 70:
            return "Moderate adherence. Try to be more consistent."
        else:
            return "Your medication adherence needs improvement. Consider setting additional reminders."

#device registration view 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_device(request):
    try:
        expo_token = request.data.get('registration_id')
        
        # Validate Expo token format
        if not expo_client.is_expo_push_token(expo_token):
            return Response(
                {'error': 'Invalid Expo push token'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update or create device registration
        device, created = UserDevice.objects.update_or_create(
            user=request.user,
            defaults={
                'expo_token': expo_token,
                'is_active': True
            }
        )

        return Response({
            'message': 'Device registered successfully',
            'device_id': device.id
        })
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )
