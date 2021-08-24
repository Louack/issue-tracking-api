from rest_framework import serializers
from django.db import IntegrityError
from rest_framework.exceptions import APIException

from .models import Project, Contributor, Issue, Comment


class ProjectSerializer(serializers.ModelSerializer):
    project_id = serializers.SerializerMethodField()
    author_info = serializers.SerializerMethodField()
    contributors = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('project_id', 'title', 'description', 'type', 'author_info', 'contributors')

    def get_project_id(self, project):
        return project.pk

    def get_author_info(self, project):
        return {'user_id': project.author.pk,
                'email': project.author.email}

    def get_contributors(self, project):
        contributors = [contributor.user.email for contributor in project.contributor_set.all()]
        return contributors

    def create(self, validated_data):
        project = super().create(validated_data)
        project.author = self.context['request_user']
        Contributor.objects.create(user=project.author,
                                   project=project,
                                   role='owner')
        project.save()
        return project


class ContributorSerializer(serializers.ModelSerializer):
    contributor_id = serializers.SerializerMethodField()
    user_info = serializers.SerializerMethodField()
    project_info = serializers.SerializerMethodField()

    class Meta:
        model = Contributor
        fields = ('contributor_id', 'project_info', 'user', 'user_info', 'role')
        extra_kwargs = {
            'user': {'write_only': True}
        }

    def get_contributor_id(self, contributor):
        return contributor.pk

    def get_project_info(self, contributor):
        return {'id': contributor.project.pk,
                'title': contributor.project.title}

    def get_user_info(self, contributor):
        return {'user_id': contributor.user.pk,
                'email': contributor.user.email}

    def validate_user(self, user):
        if self.instance:
            project = self.context['project']
            if self.instance.user == project.author:
                if self.instance.user != user:
                    raise serializers.ValidationError('En tant que créateur du projet, vous ne '
                                                      'pouvez pas vous supprimer des collaborateurs.')
        return user

    def create(self, validated_data):
        contributor = super().create(validated_data)
        contributor = self.populate_read_only_fields(contributor)
        return contributor

    def update(self, instance, validated_data):
        try:
            contributor = super().update(instance, validated_data)
        except IntegrityError:
            raise APIException('Cet utilisateur fait déjà partie du projet')
        contributor = self.populate_read_only_fields(contributor)
        return contributor

    def populate_read_only_fields(self, contributor):
        contributor.project = self.context['project']
        try:
            contributor.save()
        except IntegrityError:
            contributor.delete()
            raise APIException('Cet utilisateur fait déjà partie du projet')
        return contributor


class IssueSerializer(serializers.ModelSerializer):
    issue_id = serializers.SerializerMethodField()
    project_info = serializers.SerializerMethodField()
    author_info = serializers.SerializerMethodField()
    assignee_info = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ('issue_id', 'title', 'description', 'tag', 'priority', 'status', 'project_info',
                  'author_info', 'assignee', 'assignee_info', 'created')
        extra_kwargs = {
            'assignee': {'write_only': True}
        }

    def get_issue_id(self, issue):
        return issue.pk

    def get_author_info(self, issue):
        return {'user_id': issue.author.pk,
                'email': issue.author.email}

    def get_project_info(self, issue):
        return {'id': issue.project.pk,
                'title': issue.project.title}

    def get_assignee_info(self, issue):
        return {'user_id': issue.author.pk,
                'email': issue.author.email}

    def get_created(self, issue):
        return issue.created.strftime('%d-%m-%Y, %H:%M')

    def create(self, validated_data):
        issue = super().create(validated_data)
        issue = self.populate_read_only_fields(issue)
        return issue

    def update(self, instance, validated_data):
        issue = super().update(instance, validated_data)
        issue = self.populate_read_only_fields(issue)
        return issue

    def populate_read_only_fields(self, issue):
        issue.author = self.context['request_user']
        if not issue.assignee:
            issue.assignee = self.context['request_user']
        issue.project = self.context['project']
        issue.save()
        return issue


class CommentSerializer(serializers.ModelSerializer):
    comment_id = serializers.SerializerMethodField()
    issue_info = serializers.SerializerMethodField()
    project_info = serializers.SerializerMethodField()
    author_info = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('comment_id', 'description', 'issue_info',
                  'project_info', 'author_info', 'created')

    def get_comment_id(self, comment):
        return comment.pk

    def get_issue_info(self, comment):
        return {'id': comment.issue.pk,
                'title': comment.issue.title}

    def get_author_info(self, comment):
        return {'user_id': comment.author.pk,
                'email': comment.author.email}

    def get_project_info(self, comment):
        return {'id': comment.issue.project.pk,
                'title': comment.issue.project.title}

    def get_created(self, comment):
        return comment.created.strftime('%d-%m-%Y, %H:%M')

    def create(self, validated_data):
        comment = super().create(validated_data)
        comment = self.populate_read_only_fields(comment)
        return comment

    def update(self, instance, validated_data):
        comment = super().update(instance, validated_data)
        comment = self.populate_read_only_fields(comment)
        return comment

    def populate_read_only_fields(self, comment):
        comment.author = self.context['request_user']
        comment.issue = self.context['issue']
        comment.save()
        return comment
