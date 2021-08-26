from .views import ProjectViewset, ContributorViewset, IssueViewset, CommentViewset
from rest_framework.routers import DefaultRouter

router_projects = DefaultRouter()
router_projects.register(r'', ProjectViewset, basename='projects')

router_contributors = DefaultRouter()
router_contributors.register(r'users', ContributorViewset, basename='project-contributors')

router_issues = DefaultRouter()
router_issues.register(r'issues', IssueViewset, basename='project-issues')

router_comments = DefaultRouter()
router_comments.register(r'comments', CommentViewset, basename='issue-comments')

urlpatterns = [
    router_projects.urls,
    router_contributors.urls,
    router_issues.urls,
    router_comments
]


