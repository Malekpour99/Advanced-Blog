from rest_framework.response import Response
from .serializers import RegistrationSerializer
from rest_framework import status
from rest_framework.generics import GenericAPIView


class UserRegistration(GenericAPIView):
    """Registration for users"""

    serializer_class = RegistrationSerializer

    def post(self, request):
        """Create a new user from provided data"""
        serializer = self.serializer_class(data=request.data)
        # we can still use raise_exception=True but we tried another way for educational purposes
        if serializer.is_valid():
            serializer.save()
            # Prevention of receiving hashed password in the serializer.data
            data = {"email": serializer.validated_data["email"]}
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
