from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CaregiverRelationship, NotificationPreference

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'name', 'age', 'gender', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'age', 'gender')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'age', 'gender', 'is_staff', 'is_active')}
        ),
    )
    ordering = ['email']
    
@admin.register(CaregiverRelationship)
class CaregiverRelationshipAdmin(admin.ModelAdmin):
    model = CaregiverRelationship
    list_display = ['user', 'caregiver', 'relationship']
    fieldsets = (
        (None, {'fields': ('user', 'caregiver', 'relationship')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user', 'caregiver', 'relationship')}
        ),
    )
    ordering = ['user']
    
@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    model = NotificationPreference
    list_display = ['user', 'notification_type', 'is_enabled']
    fieldsets = (
        (None, {'fields': ('user', 'notification_type', 'is_enabled')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user', 'notification_type', 'is_enabled')}
        ),
    )
    ordering = ['user']
