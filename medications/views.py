from rest_framework import status
from rest_framework.views import APIView
from .models import Medication, Schedule
from users.models import CaregiverRelationship
from .serializers import MedicationSerializer, ScheduleSerializer
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.utils import timezone
from schedules.tasks import check_upcoming_reminders

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

########## Merge Sort Algorithm implementation for medication schedule ###########
class ScheduleListCreateView(generics.ListCreateAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_priority_weight(self, schedule):
        """
        Calculate priority weight based on medication timing and frequency
        Higher weight = higher priority
        """
        priority = 0
        current_time = timezone.now()
        schedule_time = schedule.time
        
        # Timing priority
        if schedule.timing == 'BEFORE_MEAL':
            priority += 3
        elif schedule.timing == 'AFTER_MEAL':
            priority += 2
        else:
            priority += 1
            
        # Frequency priority
        if schedule.frequency == 'DAILY':
            priority += 3
        elif schedule.frequency == 'WEEKLY':
            priority += 2
        else:
            priority += 1
            
        return priority

    def sort_schedules_by_priority(self, schedules):
        """
        Sort schedules by priority using merge sort
        """
        if len(schedules) <= 1:
            return schedules
            
        mid = len(schedules) // 2
        left = self.sort_schedules_by_priority(schedules[:mid])
        right = self.sort_schedules_by_priority(schedules[mid:])
        
        return self.merge_sorted_schedules(left, right)
    
    def merge_sorted_schedules(self, left, right):
        """
        Merge two sorted lists of schedules based on priority
        """
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            left_priority = self.get_priority_weight(left[i])
            right_priority = self.get_priority_weight(right[j])
            
            if left_priority >= right_priority:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
                
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def get_queryset(self):
        user = self.request.user
        schedules = Schedule.objects.filter(
            user=user,
            is_active=True,
            expires_at__gt=timezone.now()
        ).order_by('time')
        
        # Converting queryset to list and sort by priority
        schedules_list = list(schedules)
        return self.sort_schedules_by_priority(schedules_list)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        # Generate reminders for the newly created schedule
        schedule.generate_reminders()

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
            
            # Generate reminders for the newly created schedule
            schedule.generate_reminders()
            
            # # Trigger the check_upcoming_reminders task immediately
            try:
            #     # Trigger the check_upcoming_reminders task immediately
            #     check_upcoming_reminders.apply_async()
                result = check_upcoming_reminders()
                print(f"Check upcoming reminders result: {result}")

                # Return combined response
                return Response({
                    'medication': medication_serializer.data,
                    'schedule': schedule_serializer.data
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                print(f"Error calling check_upcoming_reminders: {str(e)}")
                # Don't return here, continue with the response


            # Return combined response
            return Response({
                'medication': medication_serializer.data,
                'schedule': schedule_serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"Error in MedicationScheduleCreateView: {str(e)}")
            if 'medication' in locals():
                medication.delete()
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

# Add an endpoint to manually generate reminders for an existing schedule
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def generate_reminders(request, schedule_id):
    try:
        schedule = Schedule.objects.get(id=schedule_id, user=request.user)
        schedule.generate_reminders()
        return Response({'message': f'Reminders generated for {schedule}'})
    except Schedule.DoesNotExist:
        return Response({'error': 'Schedule not found'}, status=404)



# caregiver view of patient medication
class PatientMedicationScheduleView(generics.ListAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        patient_id = self.request.query_params.get('user', None)
        user = self.request.user

        if not patient_id:
            return Schedule.objects.none()

        # If user is a caregiver, check if they have permission to view this patient's medications
        if user.user_type == 'CAREGIVER':
            has_permission = CaregiverRelationship.objects.filter(
                caregiver=user,
                user_id=patient_id,
                can_view_adherence=True
            ).exists()
            
            if has_permission:
                return Schedule.objects.filter(
                    user_id=patient_id,
                    is_active=True
                ).order_by('time')
            return Schedule.objects.none()
            
        # If user is viewing their own medications
        elif str(user.id) == str(patient_id):
            return Schedule.objects.filter(
                user=user,
                is_active=True
            ).order_by('time')
            
        return Schedule.objects.none()

