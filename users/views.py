from rest_framework import generics 
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, CaregiverRelationship, NotificationPreference
from .serializers import (
    CustomUserSerializer,
    CustomUserCreateSerializer,
    CaregiverRelationshipSerializer,
    NotificationPreferenceSerializer,
)

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user


class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }, status=HTTP_200_OK)
            return Response({"detail": "Invalid credentials"}, status=HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User does not exist"}, status=HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response({"detail": "Logged out successfully"}, status=HTTP_200_OK)

class CaregiverListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        relationships = CaregiverRelationship.objects.filter(user=request.user)
        serializer = CaregiverRelationshipSerializer(relationships, many=True)
        return Response(serializer.data)

class CaregiverAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CaregiverRelationshipSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class NotificationPreferenceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        preferences = NotificationPreference.objects.filter(user=request.user)
        serializer = NotificationPreferenceSerializer(preferences, many=True)
        return Response(serializer.data)

class NotificationPreferenceUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = NotificationPreferenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
