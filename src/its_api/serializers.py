from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment


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


class IssueSerializer(serializers.ModelSerializer):
    issue_id = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ('issue_id', 'description', 'tag', 'priority', 'project_id',
                  'status', 'author_user_id', 'assignee_user_id', 'created')

    def get_issue_id(self, issue):
        return issue.pk


class CommentSerializer(serializers.ModelSerializer):
    comment_id = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('comment_id', 'issue_id', 'author_user_id', 'description', 'created')

    def get_comment_id(self, comment):
        return comment.pk

