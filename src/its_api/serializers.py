from rest_framework import serializers
from .models import Project, Contributor


class ProjectSerializer(serializers.ModelSerializer):
    project_id = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('project_id', 'title', 'description', 'type', 'author_user_id')

    def get_project_id(self, project):
        return project.pk


class ContributorSerializer(serializers.ModelSerializer):
    contributor_id = serializers.SerializerMethodField()

    class Meta:
        model = Contributor
        fields = ('contributor_id', 'project_id', 'user_id', 'role')

    def get_contributor_id(self, contributor):
        return contributor.pk

