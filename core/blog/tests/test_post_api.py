from rest_framework.test import APIClient
from django.urls import reverse
import pytest


# Giving access to database
@pytest.mark.django_db
class TestPostAPI:
    def test_get_post_response_200_status(self):
        url = reverse("blog:api-v1:post-list")
        client = APIClient()
        response = client.get(url)
        assert response.status_code == 200
