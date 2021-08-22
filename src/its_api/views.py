from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .permissions import ProjectAcess, DenyProjectAcess, AuthorAccess, ObjectNotFound


class ProjectViewset(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectAcess]


class ContributorViewset(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    project = None

    def get_queryset(self):
        queryset = Contributor.objects.filter(project_id=self.project.pk)
        return queryset

    def get_project(self):
        project_id = self.kwargs['project_id']
        try:
            project = Project.objects.get(pk=project_id)
        except ObjectDoesNotExist:
            raise ObjectNotFound(f"Aucun projet ne correspond à l'identifiant n°{project_id}")
        return project

    def get_permissions(self):
        self.project = self.get_project()
        contributors = self.project.contributor_set.all()
        users = [contributor.user_id for contributor in contributors]
        if self.request.user not in users:
            self.permission_classes = [DenyProjectAcess]
        return [permission() for permission in self.permission_classes]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['kwargs'] = self.kwargs
        return context


class IssueViewset(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    project = None

    def get_queryset(self):
        queryset = Issue.objects.filter(project_id=self.project.pk)
        return queryset

    def get_project(self):
        project_id = self.kwargs['project_id']
        try:
            project = Project.objects.get(pk=project_id)
        except ObjectDoesNotExist:
            raise ObjectNotFound(f"Aucun projet ne correspond à l'identifiant n°{project_id}")
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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['kwargs'] = self.kwargs
        return context


class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    project = None
    issue = None

    def get_queryset(self):
        queryset = Comment.objects.filter(issue_id=self.issue.pk)
        return queryset

    def get_issue(self):
        project_id = self.kwargs['project_id']
        try:
            self.project = Project.objects.get(pk=project_id)
        except ObjectDoesNotExist:
            raise ObjectNotFound(f"Aucun projet ne correspond à l'identifiant n°{project_id}")
        issue_id = self.kwargs['issue_id']
        try:
            issue = Issue.objects.get(pk=issue_id)
        except ObjectDoesNotExist:
            raise ObjectNotFound(f"Aucun problème ne correspond à l'identifiant n°{issue_id}")
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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['kwargs'] = self.kwargs
        return context
