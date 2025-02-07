from rest_framework import serializers
from .models import Medication, Schedule
from users.models import CustomUser
from django.utils import timezone

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ['id', 'name', 'instructions', 'created_at']


class ScheduleSerializer(serializers.ModelSerializer):
    medication_details = MedicationSerializer(source='medication', read_only=True)
    time_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Schedule
        fields = [
            'id', 'medication','medication_id', 'user', 'user_id', 'medication_details',
            'dosage', 'time', 'time_display', 'frequency', 'timing', 'created_at', 'expires_at', 'is_active',
        ]
        read_only_fields = ['created_at', 'user']
        
    def get_time_display(self,obj):
        if obj.time:
            return{
                'iso': obj.time.isoformat(),
                'hour': obj.time.hour,
                'minute': obj.time.minute
            }
        return None
    
    def validate_expires_at(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("Expiry date cannot be in the past")
        return value
