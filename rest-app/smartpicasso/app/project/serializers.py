"""
@author p.dolata
"""

from rest_framework import serializers

from smartpicasso.app.project.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """
    Class to manage serializing Project
    """

    class Meta:
        model = Project
        fields = ('id', 'name', 'created_at', 'updated_at')
