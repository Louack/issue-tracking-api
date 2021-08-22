from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment


class ProjectSerializer(serializers.ModelSerializer):
    project_id = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    author_user_id = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('project_id', 'title', 'description', 'type', 'author', 'author_user_id')
        read_only_fields = ('author',)

    def get_project_id(self, project):
        return project.pk

    def get_author(self, project):
        return project.author.email

    def get_author_user_id(self, project):
        return project.author.pk

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
    user = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    project = serializers.SerializerMethodField()
    project_id = serializers.SerializerMethodField()

    class Meta:
        model = Contributor
        fields = ('contributor_id', 'project', 'project_id', 'user', 'user_id', 'role')
        read_only_fields = ('project',)

    def get_contributor_id(self, contributor):
        return contributor.pk

    def get_user(self, contributor):
        return contributor.user.email

    def get_user_id(self, contributor):
        return contributor.user.pk

    def get_project(self, contributor):
        return contributor.project.title

    def get_project_id(self, contributor):
        return contributor.project.pk

    def create(self, validated_data):
        contributor = super().create(validated_data)
        contributor = self.populate_read_only_fields(contributor)
        return contributor

    def update(self, instance, validated_data):
        contributor = super().update(instance, validated_data)
        contributor = self.populate_read_only_fields(contributor)
        return contributor

    def populate_read_only_fields(self, contributor):
        contributor.project = self.context['project']
        contributor.save()
        return contributor


class IssueSerializer(serializers.ModelSerializer):
    issue_id = serializers.SerializerMethodField()
    project = serializers.SerializerMethodField()
    project_id = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    author_user_id = serializers.SerializerMethodField()
    assignee = serializers.SerializerMethodField()
    assignee_user_id = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ('issue_id', 'description', 'tag', 'priority', 'status', 'project', 'project_id',
                  'author', 'author_user_id', 'assignee', 'assignee_user_id', 'created')
        read_only_fields = ('project', 'author')

    def get_issue_id(self, issue):
        return issue.pk

    def get_author(self, issue):
        return issue.author.email

    def get_author_user_id(self, issue):
        return issue.author.pk

    def get_project(self, issue):
        return issue.project.title

    def get_project_id(self, issue):
        return issue.project.pk

    def get_assignee(self, issue):
        return issue.assignee.email

    def get_assignee_user_id(self, issue):
        return issue.assignee.pk

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
    issue_id = serializers.SerializerMethodField()
    project = serializers.SerializerMethodField()
    project_id = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    author_user_id = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('comment_id', 'description', 'issue_id', 'project',
                  'project_id', 'author', 'author_user_id', 'created')
        read_only_fields = ('issue', 'author')

    def get_comment_id(self, comment):
        return comment.pk

    def get_issue_id(self, comment):
        return comment.issue.pk

    def get_author(self, comment):
        return comment.author.email

    def get_author_user_id(self, comment):
        return comment.author.pk

    def get_project(self, comment):
        return comment.issue.project.title

    def get_project_id(self, comment):
        return comment.issue.project.pk

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

