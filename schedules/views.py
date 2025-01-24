from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Reminder, AdherenceRecord
from users.models import NotificationPreference
from users.serializers import NotificationPreferenceSerializer
from .serializers import ReminderSerializer, AdherenceRecordSerializer

class ReminderListCreateView(generics.ListCreateAPIView):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated]

class ReminderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated]

class AdherenceRecordListCreateView(generics.ListCreateAPIView):
    queryset = AdherenceRecord.objects.all()
    serializer_class = AdherenceRecordSerializer
    permission_classes = [IsAuthenticated]

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
