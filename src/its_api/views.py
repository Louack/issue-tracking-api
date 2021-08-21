from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.exceptions import APIException

from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer


class ProjectViewset(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ContributorViewset(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']
    serializer_class = ContributorSerializer
    project_id = None

    def get_queryset(self):
        self.project_id = self.verify_project_id()
        queryset = Contributor.objects.filter(project_id=self.project_id)
        return queryset

    def create(self, request, *args, **kwargs):
        self.project_id = self.verify_project_id()
        if request.data['project_id'] != str(self.project_id):
            raise APIException("Ce n'est pas le bon projet")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.project_id = self.verify_project_id()
        if request.data['project_id'] != str(self.project_id):
            raise APIException("Ce n'est pas le bon projet")
        return super().update(request, *args, **kwargs)

    def verify_project_id(self):
        project_id = self.kwargs['project_id']
        try:
            Project.objects.get(pk=project_id)
        except ObjectDoesNotExist:
            raise APIException(f"Aucun projet ne correspond à l'identifiant n°{project_id}")
        return project_id


class IssueViewset(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']
    serializer_class = IssueSerializer
    project_id = None

    def get_queryset(self):
        self.project_id = self.verify_project_id()
        queryset = Issue.objects.filter(project_id=self.project_id)
        return queryset

    def create(self, request, *args, **kwargs):
        self.project_id = self.verify_project_id()
        if request.data['project_id'] != str(self.project_id):
            raise APIException("Ce n'est pas le bon projet")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.project_id = self.verify_project_id()
        if request.data['project_id'] != str(self.project_id):
            raise APIException("Ce n'est pas le bon projet")
        return super().update(request, *args, **kwargs)

    def verify_project_id(self):
        project_id = self.kwargs['project_id']
        try:
            Project.objects.get(pk=project_id)
        except ObjectDoesNotExist:
            raise APIException(f"Aucun projet ne correspond à l'identifiant n°{project_id}")
        return project_id


class CommentViewset(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']
    serializer_class = CommentSerializer
    issue_id = None

    def get_queryset(self):
        self.issue_id = self.verify_project_and_issue_ids()
        queryset = Comment.objects.filter(issue_id=self.issue_id)
        return queryset

    def create(self, request, *args, **kwargs):
        self.issue_id = self.verify_project_and_issue_ids()
        if request.data['issue_id'] != str(self.issue_id):
            raise APIException("Ce n'est pas le bon problème")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.issue_id = self.verify_project_and_issue_ids()
        if request.data['issue_id'] != str(self.issue_id):
            raise APIException("Ce n'est pas le bon problème")
        return super().update(request, *args, **kwargs)

    def verify_project_and_issue_ids(self):
        project_id = self.kwargs['project_id']
        try:
            Project.objects.get(pk=project_id)
        except ObjectDoesNotExist:
            raise APIException(f"Aucun projet ne correspond à l'identifiant n°{project_id}")
        issue_id = self.kwargs['issue_id']
        try:
            Issue.objects.get(pk=issue_id)
        except ObjectDoesNotExist:
            raise APIException(f"Aucun problème ne correspond à l'identifiant n°{issue_id}")
        return issue_id
