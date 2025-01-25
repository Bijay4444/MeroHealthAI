from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user-register'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('logout/', views.UserLogoutView.as_view(), name='user-logout'),
    path('caregivers/', views.CaregiverListView.as_view(), name='caregiver-list'),
    path('caregivers/add/', views.CaregiverAddView.as_view(), name='caregiver-add'),
    path('caregivers/<int:pk>/', views.CaregiverUpdateView.as_view(), name='caregiver-update'),
    path('notifications/', views.NotificationPreferenceView.as_view(), name='notification-preferences-detail'),
    path('notifications/update/', views.NotificationPreferenceUpdateView.as_view(), name='notification-preferences-update'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    
    path('caregiver/register/', views.CaregiverRegisterView.as_view(), name='caregiver-register'),
    path('caregiver/dashboard/', views.CaregiverDashboardView.as_view(), name='caregiver-dashboard'),
]
