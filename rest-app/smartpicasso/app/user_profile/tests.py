"""
@author: p.dolata
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from smartpicasso.app.user.models import User
from smartpicasso.app.user_profile.models import UserProfile


class UserProfileApiTest(APITestCase):
    client = APIClient()
    profile_url = reverse('profile')
    authenticate_url = reverse('authenticate')
    profile = {"username": 'test_user', "first_name": "first", "last_name": "last"}

    def test_get_profile_without_auth(self):
        response = self.client.get(self.profile_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_with_invalid_token(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.profile_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_when_user_without_profile(self):
        user = User.objects.create_user(email='test@test.com', password='test')
        self.client.force_authenticate(user=user)
        response = self.client.get(self.profile_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['success'], 'False')

    def test_get_profile(self):
        user = User.objects.create_user(email='test@test.com', password='test')
        UserProfile.objects.create(
            user=user,
            username=self.profile['username'],
            first_name=self.profile['first_name'],
            last_name=self.profile['last_name']
        )
        self.client.force_authenticate(user=user)
        response = self.client.get(self.profile_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], 'True')
        profile = response.data['profile']
        self.assertEqual(profile['username'], self.profile['username'])
        self.assertEqual(profile['first_name'], self.profile['first_name'])
        self.assertEqual(profile['last_name'], self.profile['last_name'])


class UserProfileTest(TestCase):
    profile = {"username": 'test_user', "first_name": "first", "last_name": "last"}

    def test_user_profile_str(self):
        user = User.objects.create_user(email='test@test.com', password='test')
        user_profile = UserProfile.objects.create(
            user=user,
            username=self.profile['username'],
            first_name=self.profile['first_name'],
            last_name=self.profile['last_name']
        )
        self.assertEqual(str(user_profile), 'test_user - first last')
