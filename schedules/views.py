from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Reminder, AdherenceRecord
from users.models import NotificationPreference
from users.serializers import NotificationPreferenceSerializer
from .serializers import ReminderSerializer, AdherenceRecordSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view

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
