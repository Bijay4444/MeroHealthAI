# admin.py
from django.contrib import admin
from .models import Medication, Schedule

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name', 'instructions')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('name', 'instructions')
        }),
        ('Advanced options', {
            'fields': ('created_at',),
        }),
    )
    readonly_fields = ('created_at',)
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('user', 'medication', 'dosage', 'time', 'frequency', 'is_active')
    list_filter = ('frequency', 'timing', 'is_active')
    search_fields = ('user__email', 'medication__name')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Schedule Details', {
            'fields': ('user', 'medication', 'dosage', 'time', 'frequency', 'timing')
        }),
        ('Status', {
            'fields': ('is_active', 'expires_at', )
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
