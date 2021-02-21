"""
@author: p.dolata
"""

from rest_framework import status
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from smartpicasso.app.user.serializers import UserLoginSerializer, UserRegistrationSerializer


class UserLoginView(RetrieveAPIView):
    """
    View for user login
    """
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success': 'True',
            'status_code': status.HTTP_200_OK,
            'message': 'User logged in successfully',
            'token': serializer.data['token']
        }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


class UserRegistrationView(CreateAPIView):
    """
    View for user registration
    """
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status_code': status_code,
            'message': 'User registered successfully'
        }

        return Response(response, status=status_code)
