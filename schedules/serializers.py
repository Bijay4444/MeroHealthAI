
from rest_framework import serializers
from .models import Reminder, AdherenceRecord

class ReminderSerializer(serializers.ModelSerializer):
    schedule_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Reminder
        fields = ['id', 'schedule', 'schedule_details', 'sent_time', 
                 'status', 'retry_count', 'last_retry', 'notification_sent']
        read_only_fields = ['retry_count', 'last_retry', 'notification_sent']
    
    def get_schedule_details(self, obj):
        return {
            'medication': obj.schedule.medication.name,
            'dosage': obj.schedule.dosage,
            'frequency': obj.schedule.frequency
        }

class AdherenceRecordSerializer(serializers.ModelSerializer):
    reminder_details = ReminderSerializer(source='reminder', read_only=True)
    
    class Meta:
        model = AdherenceRecord
        fields = ['id', 'reminder', 'reminder_details', 'taken_time', 
                 'status']
