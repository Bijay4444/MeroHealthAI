from rest_framework import status
from rest_framework.views import APIView
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
        # Filter medications by the logged-in user through schedules
        return Medication.objects.filter(
            schedule__user=self.request.user
        ).distinct().order_by('name')
    
    def perform_create(self, serializer):
        # Save the medication
        serializer.save()

class MedicationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MedicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only allow access to medications linked to the user's schedules
        return Medication.objects.filter(
            schedule__user=self.request.user
        ).distinct()

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
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only allow access to user's own schedules
        return Schedule.objects.filter(user=self.request.user)

# Single Endpoint for creating medication with schedule
class MedicationScheduleCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        try:
            # First create the medication
            medication_data = {
                'name': request.data.get('name'),
                'instructions': request.data.get('instructions')
            }
            medication_serializer = MedicationSerializer(data=medication_data)
            medication_serializer.is_valid(raise_exception=True)
            medication = medication_serializer.save()

            # Then create the schedule
            schedule_data = {
                'medication': medication.id,
                'dosage': request.data.get('dosage'),
                'time': request.data.get('time'),
                'frequency': request.data.get('frequency'),
                'timing': request.data.get('timing'),
                'user': request.user.id,
                'expires_at': request.data.get('expires_at')
            }
            
            schedule_serializer = ScheduleSerializer(data=schedule_data)
            schedule_serializer.is_valid(raise_exception=True)
            schedule = schedule_serializer.save(user=request.user)

            # Return combined response
            return Response({
                'medication': medication_serializer.data,
                'schedule': schedule_serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            # If anything fails, delete the medication if it was created
            if 'medication' in locals():
                medication.delete()
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)