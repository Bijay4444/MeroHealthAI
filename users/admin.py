from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CaregiverRelationship, NotificationPreference

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'name', 'age', 'gender', 'user_type', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'age', 'gender', 'user_type')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'age', 'gender', 
                      'user_type', 'is_staff', 'is_active')}
        ),
    )
    ordering = ['email']

    
@admin.register(CaregiverRelationship)
class CaregiverRelationshipAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'caregiver', 'relationship', 'permission_level',
        'emergency_contact', 'date_added'
    ]
    list_filter = ['relationship', 'permission_level', 'emergency_contact']
    search_fields = [
        'user__email', 'caregiver__email',
        'user__name', 'caregiver__name'
    ]
    readonly_fields = ['date_added', 'last_modified']
    fieldsets = (
        ('Relationship Details', {
            'fields': ('user', 'caregiver', 'relationship', 'notes')
        }),
        ('Permissions', {
            'fields': (
                'permission_level', 'can_view_adherence',
                'can_modify_schedule', 'emergency_contact'
            )
        }),
        ('Timestamps', {
            'fields': ('date_added', 'last_modified'),
            'classes': ('collapse',)
        })
    )

    
@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_notification_methods', 'quiet_hours_start', 
                   'quiet_hours_end', 'is_enabled']
    search_fields = ['user__email']
    list_filter = ['is_enabled']
    
    def get_notification_methods(self, obj):
        return ", ".join([f"{k}: {v}" for k, v in obj.notification_methods.items()])
    get_notification_methods.short_description = 'Notification Methods'