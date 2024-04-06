from django.urls import path
from . import views

app_name = "api-v1"

urlpatterns = [
    path("posts", views.post_list, name="post-list"),
    path("post/<int:id>/", views.post_detail, name="post-detail"),
]
