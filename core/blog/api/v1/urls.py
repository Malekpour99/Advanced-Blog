from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

app_name = "api-v1"


router = DefaultRouter()
router.register("post", views.PostViewSet, basename="post")
urlpatterns = router.urls

"""urlpatterns = [
    # path("post/", views.post_list, name="post-list"),
    # path("post/<int:id>/", views.post_detail, name="post-detail"),
    # path("post/", views.PostList.as_view(), name="post-list"),
    # path("post/<int:id>/", views.PostSingle.as_view(), name="post-detail"),
    # path("post/<int:pk>/", views.PostSingle.as_view(), name="post-detail"),
    path(
        "post/",
        views.PostViewSet.as_view({"get": "list", "post": "create"}),
        name="post-list",
    ),
    path(
        "post/<int:pk>/",
        views.PostViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="post-detail",
    ),
]"""
