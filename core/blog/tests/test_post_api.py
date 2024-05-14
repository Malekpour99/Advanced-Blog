from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from datetime import datetime


# Giving access to database
@pytest.mark.django_db
class TestPostAPI:
    client = APIClient()

    def test_get_post_response_200_status(self):
        url = reverse("blog:api-v1:post-list")
        response = self.client.get(url)
        assert response.status_code == 200

    def test_create_post_response_401_status(self):
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test title",
            "content": "test content",
            "published": True,
            "published_date": datetime.now(),
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code == 401
