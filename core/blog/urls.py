from django.urls import path, include
from django.views.generic import TemplateView

app_name = "blog"

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("api/v1/", include("blog.api.v1.urls")),
]
