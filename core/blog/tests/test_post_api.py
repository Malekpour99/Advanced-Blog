from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
import pytest
from datetime import datetime


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = get_user_model().objects.create_user(
        email="user@mail.com", password="commonPassword", is_verified=True
    )
    return user


# Giving access to database
@pytest.mark.django_db
class TestPostAPI:

    def test_get_post_response_200_status(self, api_client):
        url = reverse("blog:api-v1:post-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_post_response_401_status(self, api_client):
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test title",
            "content": "test content",
            "published": True,
            "published_date": datetime.now(),
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == 401

    def test_create_post_response_201_status(self, api_client, common_user):
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test title",
            "content": "test content",
            "published": True,
            "published_date": datetime.now(),
        }
        # authentication with an invalid user
        # self.client.force_authenticate(user={})
        # both 'force_authenticate' and 'force_login' can be used for authentication
        api_client.force_login(user=common_user)
        response = api_client.post(url, data, format="json")
        assert response.status_code == 201

    def test_create_invalid_post_response_400_status(self, api_client, common_user):
        url = reverse("blog:api-v1:post-list")
        invalid_data = {"title": "test title", "content": "test content"}
        api_client.force_authenticate(user=common_user)
        response = api_client.post(url, invalid_data, format="json")
        assert response.status_code == 400
