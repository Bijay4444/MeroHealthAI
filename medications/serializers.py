from rest_framework import serializers
from .models import Medication, Schedule
from users.models import CustomUser

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ['id', 'name', 'instructions']


class ScheduleSerializer(serializers.ModelSerializer):
    medication_id = serializers.PrimaryKeyRelatedField(
        queryset=Medication.objects.all(),
        source='medication',
        write_only=True
    )
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='user',
        write_only=True
    )
    medication = MedicationSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Schedule
        fields = [
            'id', 'medication', 'medication_id', 'user', 'user_id',
            'dosage', 'time', 'frequency', 'created_at', 'expires_at'
        ]
        read_only_fields = ['created_at']
