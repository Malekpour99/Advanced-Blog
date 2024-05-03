from rest_framework.response import Response
from .serializers import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
)
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from accounts.models import Profile
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail


User = get_user_model()


class UserRegistration(GenericAPIView):
    """Registration for users"""

    serializer_class = RegistrationSerializer

    def post(self, request):
        """Create a new user from provided data"""
        serializer = self.serializer_class(data=request.data)
        # we can still use raise_exception=True but we tried another way for educational purposes
        if serializer.is_valid():
            serializer.save()
            # Prevention of receiving hashed password in the serializer.data
            data = {"email": serializer.validated_data["email"]}
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(
                {"detail": "Token does not exist"}, status=status.HTTP_404_NOT_FOUND
            )


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    model = User
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"details": "password changed successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        # Since we only need one object, we override the get_object method instead of get_queryset
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class EmailTest(GenericAPIView):
    def get(self, request, *args, **kwargs):
        send_mail(
            "Email Subject",
            "This is a test email message",
            "admin@admin.com",
            ["to@user.com"],
            fail_silently=False,
        )
        return Response("Email was sent successfully")