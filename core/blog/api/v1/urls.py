from django.urls import path
from . import views

app_name = "api-v1"

urlpatterns = [
    # path("post/", views.post_list, name="post-list"),
    # path("post/<int:id>/", views.post_detail, name="post-detail"),
    path("post/", views.PostList.as_view(), name="post-list"),
    # path("post/<int:id>/", views.PostSingle.as_view(), name="post-detail"),
    path("post/<int:pk>/", views.PostSingle.as_view(), name="post-detail"),
]
