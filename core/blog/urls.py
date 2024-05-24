from django.urls import path, include
from django.views.generic import TemplateView
from . import views

app_name = "blog"

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("mock-test/", views.postman_mock_server_test, name="postman-test"),
    path("api/v1/", include("blog.api.v1.urls")),
]
