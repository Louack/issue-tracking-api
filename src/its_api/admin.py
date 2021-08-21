from django.contrib import admin
from .models import Project, Contributor, Issue, Comment


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'author_user_id',
        'type',
    )


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = (
        'project_id',
        'user_id',
        'role',
    )


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'tag',
        'priority',
        'project_id',
        'status',
        'author_user_id',
        'assignee_user_id',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'issue_id',
        'description',
        'author_user_id',
    )
