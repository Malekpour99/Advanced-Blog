from django.urls import path
from . import views
from rest_framework.authtoken.views import ObtainAuthToken

app_name = "api-v1"

urlpatterns = [
    path("registration/", views.UserRegistration.as_view(), name="registration"),
    path("token/login/", ObtainAuthToken.as_view(), name="token-login"),
]
