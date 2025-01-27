from .models import Medication, Schedule
from .serializers import MedicationSerializer, ScheduleSerializer
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone

class MedicationListCreateView(generics.ListCreateAPIView):
    serializer_class = MedicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Medication.objects.all().order_by('name')
    
class MedicationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer

class ScheduleListCreateView(generics.ListCreateAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Schedule.objects.filter(
            user=user,
            is_active=True,
            expires_at__gt=timezone.now()
        ).order_by('time')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def today(self, request):
        today = timezone.now().date()
        schedules = self.get_queryset().filter(
            time__date=today
        )
        serializer = self.get_serializer(schedules, many=True)
        return Response(serializer.data)

class ScheduleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
