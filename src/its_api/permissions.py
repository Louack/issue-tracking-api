from rest_framework.permissions import BasePermission

from .models import Issue, Comment, Contributor


class ProjectAcess(BasePermission):
    message = "Vous ne faîtes pas partie des collaborateurs de ce projet."

    def has_object_permission(self, request, view, obj):
        if type(obj) == Contributor:
            obj = obj.project
        elif type(obj) == Issue:
            obj = obj.project
        elif type(obj) == Comment:
            obj = obj.issue.project
        contributors = obj.contributor_set.all()
        users = [contributor.user for contributor in contributors]
        return request.user in users


class ProjectOwnerAccess(BasePermission):
    message = "Seul le créateur de ce projet peut ajouter/modifier/supprimer des collaborateurs"

    def has_permission(self, request, view):
        project = view.get_project()
        if view.action not in ['list', 'retrieve']:
            return request.user == project.author
        else:
            return True


class AuthorAccess(BasePermission):
    message = "Vous n'êtes pas le créateur de ce projet/problème/commentaire."

    def has_object_permission(self, request, view, obj):
        if view.action != 'retrieve':
            return request.user == obj.author
        else:
            return True
