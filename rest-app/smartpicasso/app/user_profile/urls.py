"""
@author: p.dolata
"""

from django.conf.urls import url

from smartpicasso.app.user_profile.views import UserProfileView

urlpatterns = [
    url(r'^profile', UserProfileView.as_view(), name='profile')
]
