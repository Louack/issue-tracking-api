from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.exceptions import APIException

from .models import Project, Contributor
from .serializers import ProjectSerializer, ContributorSerializer


class ProjectView(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ContributorView(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']
    serializer_class = ContributorSerializer
    project = None

    def get_queryset(self):
        self.project = self.get_project()
        queryset = Contributor.objects.filter(project_id=self.project.pk)
        return queryset

    def create(self, request, *args, **kwargs):
        self.project = self.get_project()
        if request.data['project_id'] != str(self.project.pk):
            raise APIException("Ce n'est pas le bon projet")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.project = self.get_project()
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

