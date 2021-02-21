"""
@author: p.dolata
"""

from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from smartpicasso.app.user_profile.models import UserProfile


class UserProfileView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'True',
                'status_code': status_code,
                'message': 'User profile fetched successfully',
                'profile': {
                    'username': user_profile.username,
                    'first_name': user_profile.first_name,
                    'last_name': user_profile.last_name
                }
            }
        except Exception as e:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                'success': 'False',
                'status_code': status_code,
                'message': 'User profile does not exist',
                'error': str(e)
            }
        return Response(response, status=status_code)
