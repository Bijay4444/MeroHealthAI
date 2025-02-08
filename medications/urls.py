from django.urls import path
from .views import (
    MedicationListCreateView,
    MedicationRetrieveUpdateDestroyView,
    ScheduleListCreateView,
    ScheduleRetrieveUpdateDestroyView,
    MedicationScheduleCreateView
)

urlpatterns = [
    path('', MedicationListCreateView.as_view(), name='medication-list-create'),
    path('<int:pk>/', MedicationRetrieveUpdateDestroyView.as_view(), name='medication-detail'),
    path('schedules/', ScheduleListCreateView.as_view(), name='schedule-list-create'),
    path('schedules/<int:pk>/', ScheduleRetrieveUpdateDestroyView.as_view(), name='schedule-detail'),
    path('create-with-schedule/', MedicationScheduleCreateView.as_view(), name='medication-schedule-create'),
]
