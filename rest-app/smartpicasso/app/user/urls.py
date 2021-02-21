"""
@author: p.dolata
"""

from django.conf.urls import url

from smartpicasso.app.user.views import UserLoginView, UserRegistrationView

urlpatterns = [
    url(r'^authenticate', UserLoginView.as_view(), name='authenticate'),
    url(r'^register', UserRegistrationView.as_view(), name='register')
]
