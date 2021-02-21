"""
@author p.dolata
"""

import uuid

from django.db import models

from smartpicasso.app.user.models import User


class Project(models.Model):
    """
    Model representing user's project
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        """
        Meta to set table name in database
        """
        db_table = 'project'
