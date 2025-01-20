from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user-register'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('logout/', views.UserLogoutView.as_view(), name='user-logout'),
    path('caregivers/', views.CaregiverListView.as_view(), name='caregiver-list'),
    path('caregivers/add/', views.CaregiverAddView.as_view(), name='caregiver-add'),
    path('notifications/<int:pk>/', views.NotificationPreferenceView.as_view(), name='notification-preferences-detail'),
    path('notifications/<int:pk>/update/', views.NotificationPreferenceView.as_view(), name='notification-preferences-update'),
]
