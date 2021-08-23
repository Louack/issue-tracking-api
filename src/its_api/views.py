from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets

from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .permissions import ProjectAcess, AuthorAccess, ProjectOwnerAccess
from .exceptions import ObjectNotFound, BadRequest


class ProjectViewset(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [ProjectAcess, AuthorAccess]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request_user'] = self.request.user
        return context


class ContributorViewset(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [ProjectAcess, ProjectOwnerAccess]
    project = None

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.project = self.get_project()

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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['project'] = self.project
        return context

    def perform_destroy(self, instance):
        if instance.user == self.project.author:
            raise BadRequest('En tant que créateur du projet, vous ne pouvez pas vous supprimer des collaborateurs.')
        return super().perform_destroy(instance)


class IssueViewset(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [ProjectAcess, AuthorAccess]
    project = None

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.project = self.get_project()

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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request_user'] = self.request.user
        context['project'] = self.project
        return context


class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [ProjectAcess, AuthorAccess]
    issue = None

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.issue = self.get_issue()

    def get_queryset(self):
        queryset = Comment.objects.filter(issue_id=self.issue.pk)
        return queryset

    def get_issue(self):
        project_id = self.kwargs['project_id']
        try:
            Project.objects.get(pk=project_id)
        except ObjectDoesNotExist:
            raise ObjectNotFound(f"Aucun projet ne correspond à l'identifiant n°{project_id}.")
        issue_id = self.kwargs['issue_id']
        try:
            issue = Issue.objects.get(pk=self.kwargs['issue_id'])
        except ObjectDoesNotExist:
            raise ObjectNotFound(f"Aucun problème ne correspond à l'identifiant n°{issue_id}.")
        if not issue.project.pk == project_id:
            raise ObjectNotFound(f"Le projet n°{project_id} ne comprend pas de problème n°{issue_id}. ")
        return issue

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request_user'] = self.request.user
        context['issue'] = self.issue
        return context
