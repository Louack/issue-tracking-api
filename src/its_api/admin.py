from django.contrib import admin
from .models import Project, Contributor, Issue, Comment


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'author',
        'type',
    )


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = (
        'project',
        'user',
        'role',
    )


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'tag',
        'priority',
        'project',
        'status',
        'author',
        'assignee',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'issue',
        'description',
        'author',
    )
