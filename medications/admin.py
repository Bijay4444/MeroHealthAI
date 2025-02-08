# admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Medication, Schedule

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'instructions_preview', 'associated_users', 'created_at')
    list_filter = ('created_at', 'schedule__user')
    search_fields = ('name', 'instructions', 'schedule__user__email', 'schedule__user__name')
    readonly_fields = ('created_at',)
    
    def instructions_preview(self, obj):
        return obj.instructions[:50] + '...' if len(obj.instructions) > 50 else obj.instructions
    instructions_preview.short_description = 'Instructions'
    
    def associated_users(self, obj):
        users = obj.schedule_set.values_list('user__name', flat=True).distinct()
        return ', '.join(users) if users else 'No users'
    associated_users.short_description = 'Users'
    
    fieldsets = (
        (None, {
            'fields': ('name', 'instructions')
        }),
        ('Advanced options', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('user', 'medication_name', 'dosage', 'formatted_time', 
                   'frequency', 'timing', 'status_badge', 'created_at')
    list_filter = ('frequency', 'timing', 'is_active', 'created_at', 'user')
    search_fields = ('user__email', 'user__name', 'medication__name', 'dosage')
    readonly_fields = ('created_at',)
    list_per_page = 20
    
    def medication_name(self, obj):
        return obj.medication.name
    medication_name.short_description = 'Medication'
    
    def formatted_time(self, obj):
        return obj.time.strftime('%I:%M %p') if obj.time else '-'
    formatted_time.short_description = 'Time'
    
    def status_badge(self, obj):
        if obj.is_active:
            if obj.expires_at and obj.expires_at < timezone.now():
                return format_html(
                    '<span style="background-color: #ffd700; padding: 3px 10px; border-radius: 10px;">'
                    'Expired</span>'
                )
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 10px;">'
                'Active</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 3px 10px; border-radius: 10px;">'
            'Inactive</span>'
        )
    status_badge.short_description = 'Status'

    fieldsets = (
        ('Basic Information', {
            'fields': (('user', 'medication'), ('dosage', 'time'))
        }),
        ('Schedule Details', {
            'fields': (('frequency', 'timing'), 'is_active')
        }),
        ('Advanced', {
            'fields': ('expires_at', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_active', 'make_inactive']
    
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Mark selected schedules as active"
    
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Mark selected schedules as inactive"
