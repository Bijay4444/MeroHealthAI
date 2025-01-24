# schedules/urls.py

from django.urls import path
from .views import (
    ReminderListCreateView,
    ReminderRetrieveUpdateDestroyView,
    AdherenceRecordListCreateView,
    AdherenceRecordRetrieveUpdateDestroyView,
    NotificationPreferenceDetailView,
)

urlpatterns = [
    path('reminders/', ReminderListCreateView.as_view(), name='reminder-list-create'),
    path('reminders/<int:pk>/', ReminderRetrieveUpdateDestroyView.as_view(), name='reminder-detail'),
    path('adherence-records/', AdherenceRecordListCreateView.as_view(), name='adherence-record-list-create'),
    path('adherence-records/<int:pk>/', AdherenceRecordRetrieveUpdateDestroyView.as_view(), name='adherence-record-detail'),
    path('notification-preferences/', NotificationPreferenceDetailView.as_view(), name='notification-preference-detail'),
]
