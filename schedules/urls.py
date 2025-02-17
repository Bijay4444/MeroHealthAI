from django.urls import path
from .views import (
    ReminderListCreateView,
    ReminderRetrieveUpdateDestroyView,
    AdherenceRecordListCreateView,
    AdherenceRecordRetrieveUpdateDestroyView,
    NotificationPreferenceDetailView,
    MedicationAdherenceScoreView
)
from .views import upcoming_reminders, mark_reminder_taken, register_device

urlpatterns = [
    path('reminders/', ReminderListCreateView.as_view(), name='reminder-list-create'),
    path('reminders/<int:pk>/', ReminderRetrieveUpdateDestroyView.as_view(), name='reminder-detail'),
    path('reminders/upcoming/', upcoming_reminders, name='upcoming-reminders'),
    path('reminders/<int:pk>/mark-taken/', mark_reminder_taken, name='mark-reminder-taken'),
    
    path('adherence-records/', AdherenceRecordListCreateView.as_view(), name='adherence-record-list-create'),
    path('adherence-records/<int:pk>/', AdherenceRecordRetrieveUpdateDestroyView.as_view(), name='adherence-record-detail'),
    path('adherence-score/', MedicationAdherenceScoreView.as_view(), name='adherence-score'),

    path('notification-preferences/', NotificationPreferenceDetailView.as_view(), name='notification-preference-detail'),

    path('devices/register/', register_device, name='register-device'),
]
