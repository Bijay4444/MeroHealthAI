from rest_framework import serializers
from .models import CustomUser, NotificationPreference, CaregiverRelationship

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'name', 'age', 'gender', 'user_type', 'is_active', 'is_staff']
        extra_kwargs = {
            'is_active': {'read_only': True},
            'is_staff': {'read_only': True},
        }

class CustomUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'name', 'age', 'gender', 'user_type']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data.get('user_type') not in ['PATIENT', 'CAREGIVER']:
            raise serializers.ValidationError("Invalid user type")
        return data
    
    def create(self, validated_data):
        """
        Override the default create method to hash the password.
        """
        password = validated_data.pop('password')  # Extract password
        user = CustomUser(**validated_data)       # Create user instance
        user.set_password(password)               # Hash password
        user.save()                               # Save the user
        return user

class NotificationPreferenceSerializer(serializers.ModelSerializer):
    notification_methods = serializers.JSONField(default=dict)
    
    class Meta:
        model = NotificationPreference
        fields = ['id', 'user', 'notification_methods', 'quiet_hours_start', 
                 'quiet_hours_end', 'is_enabled']
        extra_kwargs = {
            'user': {'required': False},
            'notification_methods': {'required': False}
        }

    def validate_notification_methods(self, value):
        valid_types = ['EMAIL', 'SMS', 'PUSH']
        if not isinstance(value, dict):
            raise serializers.ValidationError("Notification methods must be a dictionary")
        for key in value.keys():
            if key not in valid_types:
                raise serializers.ValidationError(f"Invalid notification type: {key}")
        return value
    
    def create(self, validated_data):
        if 'notification_methods' not in validated_data:
            validated_data['notification_methods'] = {
                'EMAIL': False,
                'SMS': False,
                'PUSH': True
            }
        if 'user' not in validated_data:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)



class CaregiverRelationshipSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    caregiver_email = serializers.EmailField(source='caregiver.email', read_only=True)
    relationship_display = serializers.CharField(source='get_relationship_display', read_only=True)
    permission_level_display = serializers.CharField(source='get_permission_level_display', read_only=True)

    class Meta:
        model = CaregiverRelationship
        fields = [
            'id', 'user', 'caregiver', 'user_email', 'caregiver_email',
            'relationship', 'relationship_display', 'permission_level',
            'permission_level_display', 'can_view_adherence',
            'can_modify_schedule', 'emergency_contact', 'notes',
            'date_added', 'last_modified'
        ]
        read_only_fields = ['date_added', 'last_modified']
