from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.exceptions import APIException

from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .permissions import ProjectAcess, DenyProjectAcess, AuthorAccess


class ProjectViewset(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [ProjectAcess]


class ContributorViewset(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    project = None

    def get_queryset(self):
        queryset = Contributor.objects.filter(project_id=self.project.pk)
        return queryset

    def create(self, request, *args, **kwargs):
        if request.data['project_id'] != str(self.project.pk):
            raise APIException("Ce n'est pas le bon projet")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.data['project_id'] != str(self.project.pk):
            raise APIException("Ce n'est pas le bon projet")
        return super().update(request, *args, **kwargs)

    def get_project(self):
        project_id = self.kwargs['project_id']
        try:
            project = Project.objects.get(pk=project_id)
        except ObjectDoesNotExist:
            raise APIException(f"Aucun projet ne correspond à l'identifiant n°{project_id}")
        return project

    def get_permissions(self):
        self.project = self.get_project()
        contributors = self.project.contributor_set.all()
        users = [contributor.user_id for contributor in contributors]
        if self.request.user not in users:
            self.permission_classes = [DenyProjectAcess]
        return [permission() for permission in self.permission_classes]


class IssueViewset(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    project = None

    def get_queryset(self):
        queryset = Issue.objects.filter(project_id=self.project.pk)
        return queryset

    def create(self, request, *args, **kwargs):
        if request.data['project_id'] != str(self.project.pk):
            raise APIException("Ce n'est pas le bon projet")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.data['project_id'] != str(self.project.pk):
            raise APIException("Ce n'est pas le bon projet")
        return super().update(request, *args, **kwargs)

    def get_project(self):
        project_id = self.kwargs['project_id']
        try:
            project = Project.objects.get(pk=project_id)
        except ObjectDoesNotExist:
            raise APIException(f"Aucun projet ne correspond à l'identifiant n°{project_id}")
        return project

    def get_permissions(self):
        self.project = self.get_project()
        contributors = self.project.contributor_set.all()
        users = [contributor.user_id for contributor in contributors]
        if self.request.user not in users:
            self.permission_classes = [DenyProjectAcess]
        else:
            if not self.action == 'retrieve':
                self.permission_classes = [AuthorAccess]
        return [permission() for permission in self.permission_classes]


class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    project = None
    issue = None

    def get_queryset(self):
        queryset = Comment.objects.filter(issue_id=self.issue.pk)
        return queryset

    def create(self, request, *args, **kwargs):
        if request.data['issue_id'] != str(self.issue.pk):
            raise APIException("Ce n'est pas le bon problème")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.data['issue_id'] != str(self.issue.pk):
            raise APIException("Ce n'est pas le bon problème")
        return super().update(request, *args, **kwargs)

    def get_issue(self):
        project_id = self.kwargs['project_id']
        try:
            self.project = Project.objects.get(pk=project_id)
        except ObjectDoesNotExist:
            raise APIException(f"Aucun projet ne correspond à l'identifiant n°{project_id}")
        issue_id = self.kwargs['issue_id']
        try:
            issue = Issue.objects.get(pk=issue_id)
        except ObjectDoesNotExist:
            raise APIException(f"Aucun problème ne correspond à l'identifiant n°{issue_id}")
        return issue

    def get_permissions(self):
        self.issue = self.get_issue()
        contributors = self.project.contributor_set.all()
        users = [contributor.user_id for contributor in contributors]
        if self.request.user not in users:
            self.permission_classes = [DenyProjectAcess]
        else:
            if not self.action == 'retrieve':
                self.permission_classes = [AuthorAccess]
        return [permission() for permission in self.permission_classes]
