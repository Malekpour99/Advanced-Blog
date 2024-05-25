from django.http import JsonResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
import requests


def postman_mock_server_test_demo(request):
    if cache.get("test_delay_api") is None:
        response = requests.get(
            "https://0e0ecd6a-4a53-4847-86ad-60cdb6dccedd.mock.pstmn.io/test/delay/5"
        )
        # You can set the timeout locally as well (default: 5 minutes globally)
        cache.set("test_delay_api", response.json(), 120)
    return JsonResponse(cache.get("test_delay_api"))


# Proper way to cache response
@cache_page(60)
def postman_mock_server_test(request):
    response = requests.get(
        "https://0e0ecd6a-4a53-4847-86ad-60cdb6dccedd.mock.pstmn.io/test/delay/5"
    )
    return JsonResponse(response.json())
