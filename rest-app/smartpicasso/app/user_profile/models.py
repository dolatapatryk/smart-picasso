"""
@author p.dolata
"""

import uuid
from django.db import models
from smartpicasso.app.user.models import User


class UserProfile(models.Model):
    """
    Model representing user's profile
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, unique=False)
    last_name = models.CharField(max_length=50, unique=False)

    def __str__(self):
        return str(self.username) + ' - ' + str(self.first_name) + ' ' + str(self.last_name)

    class Meta:
        """
        Meta to set table name in database
        """
        db_table = 'user_profile'
