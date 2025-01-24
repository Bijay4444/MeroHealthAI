
from rest_framework import serializers
from .models import Reminder, AdherenceRecord

class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ['id', 'schedule', 'sent_time', 'status']

class AdherenceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdherenceRecord
        fields = ['id', 'reminder', 'taken_time', 'status']


