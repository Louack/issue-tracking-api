from rest_framework.permissions import BasePermission


class ProjectOwnerAccess(BasePermission):
    message = "Seul le créateur de ce projet peut ajouter/modifier/supprimer des collaborateurs."

    def has_permission(self, request, view):
        if view.action not in ['list', 'retrieve']:
            return request.user == view.project.author
        else:
            return True


class AuthorAccess(BasePermission):
    message = "Vous n'êtes pas le créateur de ce projet/problème/commentaire."

    def has_object_permission(self, request, view, obj):
        if view.action != 'retrieve':
            return request.user == obj.author
        else:
            return True
