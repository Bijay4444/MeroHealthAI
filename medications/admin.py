# admin.py
from django.contrib import admin
from .models import Medication, Schedule

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('user', 'medication', 'dosage', 'time', 'frequency', 'created_at', 'expires_at')
    list_filter = ('user', 'medication', 'frequency')
    search_fields = ('user__name', 'medication__name')
