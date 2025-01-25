
from rest_framework.permissions import BasePermission

class IsCaregiverPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'CAREGIVER'

class HasCaregiverPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        if request.user.user_type == 'CAREGIVER':
            relationship = CaregiverRelationship.objects.filter(
                caregiver=request.user,
                user=obj.user
            ).first()
            return relationship and relationship.can_modify_schedule
        return False
