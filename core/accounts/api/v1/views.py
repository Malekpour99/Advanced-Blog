from rest_framework.response import Response
from .serializers import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    ActivationResendSerializer,
)
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from accounts.models import Profile
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage
from ..utils import EmailThread
import jwt
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


# from mail_templated import send_mail
# from django.core.mail import send_mail


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
            email = serializer.validated_data["email"]
            # Prevention of receiving hashed password in the serializer.data
            data = {"email": email}
            user_obj = get_object_or_404(User, email=email)
            ActivationEmailSender.send_activation_email(request, user_obj)
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        """Return an access token based on the user"""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ActivationAPIView(APIView):
    """Decoding JWT authentication token and activating user"""

    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id", None)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(
                {"details": "Token has been expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.exceptions.InvalidSignatureError:
            return Response(
                {"details": "Token is not valid"}, status=status.HTTP_400_BAD_REQUEST
            )
        user_obj = User.objects.get(pk=user_id)
        if user_obj.is_verified:
            return Response(
                {"details": "Your account has already been verified and is active"}
            )
        user_obj.is_verified = True
        user_obj.save()
        return Response({"details": "Your account has been verified and activated"})


class ActivationResendAPIView(GenericAPIView):
    """Resending JWT authentication token for user activation"""

    serializer_class = ActivationResendSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        ActivationEmailSender.send_activation_email(request, user_obj)
        return Response(
            {"details": "Activation link resent was successful"},
            status=status.HTTP_200_OK,
        )


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
        """Sending an email containing the access token based on the user email"""
        self.email = "user@mail.com"
        user_obj = get_object_or_404(User, email=self.email)
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage(
            "email/hello.tpl", {"token": token}, "admin@admin.com", to=[self.email]
        )
        EmailThread(email_obj).start()
        return Response("Email was sent successfully")

    def get_tokens_for_user(self, user):
        """Return an access token based on the user"""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ActivationEmailSender:
    @staticmethod
    def send_activation_email(request, user):
        """Send activation email to the user"""
        token = ActivationEmailSender.get_tokens_for_user(user)
        current_site = get_current_site(request)
        protocol = "https" if request.is_secure() else "http"
        domain = current_site.domain
        email_obj = EmailMessage(
            "email/activation-email.tpl",
            {"protocol": protocol, "domain": domain, "token": token},
            "admin@admin.com",
            to=[user.email],
        )
        EmailThread(email_obj).start()

    @staticmethod
    def get_tokens_for_user(user):
        """Return an access token based on the user"""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
