"""
@author p.dolata
"""

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from smartpicasso.app.project.serializers import ProjectSerializer
from smartpicasso.app.project.models import Project


class ProjectsView(ModelViewSet):
    """
    View for project endpoints
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(user=user)
