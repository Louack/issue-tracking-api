from django.contrib import admin
from .models import Project, Contributor


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
