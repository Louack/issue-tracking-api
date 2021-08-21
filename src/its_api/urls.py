from .views import ProjectView, ContributorView
from rest_framework.routers import DefaultRouter

router_projects = DefaultRouter()
router_projects.register(r'projects', ProjectView, basename='projects')

router_contributors = DefaultRouter()
router_contributors.register(r'users', ContributorView, basename='project-contributors')

urlpatterns = [router_projects.urls, router_contributors.urls]

