"""
@author: p.dolata
"""

from rest_framework.routers import SimpleRouter

from smartpicasso.app.project.views import ProjectsView

router = SimpleRouter(trailing_slash=False)
router.register('projects', ProjectsView, basename="projects")
urlpatterns = router.urls
