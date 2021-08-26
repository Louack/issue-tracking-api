from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from users.models import CustomUser
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .permissions import AuthorAccess, ProjectOwnerAccess
from .exceptions import ObjectNotFound, BadRequest


class ProjectViewset(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, AuthorAccess]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request_user'] = self.request.user
        return context

    def get_queryset(self):
        queryset = Project.objects.filter(contributor__user=self.request.user.pk)
        return queryset


class ContributorViewset(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options', 'trace']
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, ProjectOwnerAccess]
    project = None

    def initial(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.project = self.get_project()
        super().initial(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Contributor.objects.filter(project_id=self.project.pk)
        return queryset

    def get_project(self):
        project_id = self.kwargs['project_id']
        try:
            project = Project.objects.get(pk=project_id)
        except ObjectDoesNotExist:
            raise ObjectNotFound('Not found')
        self.contributors = CustomUser.objects.filter(contributor__project=project.pk)
        if self.request.user not in self.contributors:
            raise ObjectNotFound('Not found')
        return project

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['project'] = self.project
        context['contributors'] = self.contributors
        return context

    def perform_destroy(self, instance):
        if instance.user == self.project.author:
            raise BadRequest('En tant que créateur du projet, vous ne pouvez pas vous supprimer des collaborateurs.')
        return super().perform_destroy(instance)


class IssueViewset(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, AuthorAccess]
    project = None

    def initial(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.project = self.get_project()
        super().initial(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Issue.objects.filter(project_id=self.project.pk)
        return queryset

    def get_project(self):
        project_id = self.kwargs['project_id']
        try:
            project = Project.objects.get(pk=project_id)
        except ObjectDoesNotExist:
            raise ObjectNotFound('Not found')
        contributors = CustomUser.objects.filter(contributor__project=project.pk)
        if self.request.user not in contributors:
            raise ObjectNotFound('Not found')
        return project

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request_user'] = self.request.user
        context['project'] = self.project
        return context


class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, AuthorAccess]
    project = None
    issue = None

    def initial(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.project = self.get_project()
            self.issue = self.get_issue()
        super().initial(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Comment.objects.filter(issue_id=self.issue.pk)
        return queryset

    def get_project(self):
        project_id = self.kwargs['project_id']
        try:
            project = Project.objects.get(pk=project_id)
        except ObjectDoesNotExist:
            raise ObjectNotFound('Not found')
        contributors = CustomUser.objects.filter(contributor__project=project.pk)
        if self.request.user not in contributors:
            raise ObjectNotFound('Not found')
        return project

    def get_issue(self):
        issue_id = self.kwargs['issue_id']
        try:
            issue = Issue.objects.get(pk=issue_id)
        except ObjectDoesNotExist:
            raise ObjectNotFound('Not found')
        project_id = self.kwargs['project_id']
        if issue.project.pk != project_id:
            raise ObjectNotFound('Not found')
        return issue

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request_user'] = self.request.user
        context['issue'] = self.issue
        return context
