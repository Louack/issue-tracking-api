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
        read_only_fields = ('project_id',)

    def get_contributor_id(self, contributor):
        return contributor.pk

    def create(self, validated_data):
        contributor = super().create(validated_data)
        contributor = self.populate_read_only_fields(contributor)
        return contributor

    def update(self, instance, validated_data):
        contributor = super().update(instance, validated_data)
        contributor = self.populate_read_only_fields(contributor)
        return contributor

    def populate_read_only_fields(self, contributor):
        contributor.project_id = self.context['project']
        contributor.save()
        return contributor


class IssueSerializer(serializers.ModelSerializer):
    issue_id = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ('issue_id', 'description', 'tag', 'priority', 'project_id',
                  'status', 'author_user_id', 'assignee_user_id', 'created')
        read_only_fields = ('project_id', 'author_user_id')

    def get_issue_id(self, issue):
        return issue.pk

    def create(self, validated_data):
        issue = super().create(validated_data)
        issue = self.populate_read_only_fields(issue)
        return issue

    def update(self, instance, validated_data):
        issue = super().update(instance, validated_data)
        issue = self.populate_read_only_fields(issue)
        return issue

    def populate_read_only_fields(self, issue):
        issue.author_user_id = self.context['request_user']
        if not issue.assignee_user_id:
            issue.assignee_user_id = self.context['request_user']
        issue.project_id = self.context['project']
        issue.save()
        return issue


class CommentSerializer(serializers.ModelSerializer):
    comment_id = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('comment_id', 'issue_id', 'author_user_id', 'description', 'created')
        read_only_fields = ('issue_id', 'author_user_id')

    def get_comment_id(self, comment):
        return comment.pk

    def create(self, validated_data):
        comment = super().create(validated_data)
        comment = self.populate_read_only_fields(comment)
        return comment

    def update(self, instance, validated_data):
        comment = super().update(instance, validated_data)
        comment = self.populate_read_only_fields(comment)
        return comment

    def populate_read_only_fields(self, comment):
        comment.author_user_id = self.context['request_user']
        comment.issue_id = self.context['issue']
        comment.save()
        return comment

