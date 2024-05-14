from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from datetime import datetime


@pytest.fixture
def api_client():
    client = APIClient()
    return client


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
