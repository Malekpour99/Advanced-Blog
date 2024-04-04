from django.urls import path
from . import views

app_name = "api-v1"

urlpatterns = [
    path("", views.api_rest_view, name="test"),
]
