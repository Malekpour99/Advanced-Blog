from django.http import JsonResponse
import requests


def postman_mock_server_test(request):
    response = requests.get(
        "https://0e0ecd6a-4a53-4847-86ad-60cdb6dccedd.mock.pstmn.io/test/delay/5"
    )
    return JsonResponse(response.json())
