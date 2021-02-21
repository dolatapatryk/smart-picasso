"""
@author: p.dolata
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from smartpicasso.app.user.models import User
from smartpicasso.app.user.serializers import UserLoginSerializer, UserRegistrationSerializer
from smartpicasso.app.user_profile.models import UserProfile


class UserApiTest(APITestCase):
    client = APIClient()
    authenticate_url = reverse('authenticate')
    register_url = reverse('register')
    profile = {"username": 'test', "first_name": "test", "last_name": "test"}

    def test_login_when_user_non_exist(self):
        response = self.client.post(self.authenticate_url, {'email': 'non-exist', 'password': '123'}, format='json')
        assert response.status_code == 400

    def test_login_when_user_exist(self):
        User.objects.create_user(email='test@test.com', password='test')
        response = self.client.post(self.authenticate_url, {'email': 'test@test.com', 'password': 'test'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], 'True')
        self.assertIn('token', response.data)

    def test_register_when_user_non_exist(self):
        response = self.client.post(self.register_url, {'email': 'test@test.com', 'password': 'test',
                                                        'profile': self.profile}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['success'], 'True')

    def test_register_when_email_exist(self):
        User.objects.create_user(email='test@test.com', password='test')
        response = self.client.post(self.register_url, {'email': 'test@test.com', 'password': 'test',
                                                        'profile': self.profile}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_register_when_username_exist(self):
        user = User.objects.create_user(email='test2@test.com', password='test')
        UserProfile.objects.create(
            user=user,
            username=self.profile['username'],
            first_name=self.profile['first_name'],
            last_name=self.profile['last_name']
        )
        response = self.client.post(self.register_url, {'email': 'test@test.com', 'password': 'test',
                                                        'profile': self.profile}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('profile', response.data)
        self.assertIn('username', response.data['profile'])


class UserTest(TestCase):

    def test_user_str(self):
        email = 'test@test.com'
        user = User.objects.create_user(email=email, password='test')
        self.assertEqual(str(user), email)


class UserLoginSerializerTest(TestCase):
    serializer = UserLoginSerializer()

    def test_validate_wrong_credentials(self):
        data = {'email': 'test@test.com', 'password': '123'}
        self.assertRaises(serializers.ValidationError, self.serializer.validate, data)

    def test_validate_success(self):
        User.objects.create_user(email='test@test.com', password='test')
        data = {'email': 'test@test.com', 'password': 'test'}
        result = self.serializer.validate(data)
        self.assertEqual(result['email'], 'test@test.com')
        self.assertIn('token', result)


class UserRegistrationSerializerTest(TestCase):
    serializer = UserRegistrationSerializer()

    def test_create(self):
        profile = {"username": 'test', "first_name": "test", "last_name": "test"}
        user = self.serializer.create({"email": "test@test.com", "password": "test", "profile": profile})

        self.assertNotEqual(user, None)
        self.assertEqual(user.email, "test@test.com")


class UserManagerTest(TestCase):
    manager = User.objects

    def test_create_user_none_email(self):
        email = None
        self.assertRaises(ValueError, self.manager.create_user, email)

    def test_create_user(self):
        user = self.manager.create_user("test@test.pl", "test")
        self.assertNotEqual(user, None)
        self.assertEqual(user.email, "test@test.pl")
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.is_staff, False)

    def test_create_superuser_none_password(self):
        password = None
        self.assertRaises(TypeError, self.manager.create_superuser, "super@test.pl", password)

    def test_create_superuser(self):
        user = self.manager.create_superuser("super@test.pl", "test")
        self.assertNotEqual(user, None)
        self.assertEqual(user.email, "super@test.pl")
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_superuser, True)
        self.assertEqual(user.is_staff, True)
