from django.contrib import admin
from .models import Reminder, AdherenceRecord

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'sent_time', 'status', 'notification_sent')
    list_filter = ('status', 'notification_sent')
    search_fields = ('schedule__user__email', 'schedule__medication__name')
    readonly_fields = ('retry_count', 'last_retry')

@admin.register(AdherenceRecord)
class AdherenceRecordAdmin(admin.ModelAdmin):
    list_display = ('reminder', 'taken_time', 'status')
    list_filter = ('status',)
    search_fields = ('reminder__schedule__user__email',)
    readonly_fields = ('taken_time',)