"""
@author: p.dolata
"""

from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from smartpicasso.app.project.models import Project
from smartpicasso.app.user.models import User


class ProjectsApiTest(APITestCase):
    client = APIClient()
    projects_url = reverse('projects-list')
    new_project = {'name': 'test_project'}

    def test_create_project_without_auth(self):
        response = self.client.post(self.projects_url, self.new_project, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_project_with_invalid_token(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(self.projects_url, self.new_project, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_project(self):
        user = User.objects.create_user(email='test@test.com', password='test')
        self.client.force_authenticate(user=user)
        response = self.client.post(self.projects_url, self.new_project, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        project = Project.objects.get(id=response.data['id'])
        self.assertEqual(project.user.id, user.id)
        self.assertEqual(project.name, self.new_project['name'])
        self.assertAlmostEqual(datetime.timestamp(project.created_at), datetime.timestamp(datetime.now()),
                               delta=600)
        self.assertAlmostEqual(datetime.timestamp(project.updated_at), datetime.timestamp(datetime.now()),
                               delta=600)

    def test_get_user_projects_without_auth(self):
        response = self.client.get(self.projects_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_projects_with_invalid_token(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.projects_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_projects(self):
        user = User.objects.create_user(email='test@test.com', password='test')
        self.client.force_authenticate(user=user)
        Project.objects.create(user=user, name='project_1')
        Project.objects.create(user=user, name='project_2')
        response = self.client.get(self.projects_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        projects = response.data
        self.assertEqual(len(projects), 2)
        self.assertEqual(projects[0]['name'], 'project_1')
        self.assertEqual(projects[1]['name'], 'project_2')


class ProjectTest(TestCase):

    def test_project_str(self):
        user = User.objects.create_user(email='test@test.com', password='test')
        project = Project.objects.create(user=user, name='test_project')
        self.assertEqual(str(project), 'test_project')
