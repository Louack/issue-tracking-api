from rest_framework.permissions import BasePermission


class ProjectAcess(BasePermission):
    message = "Vous ne faîtes pas partie des collaborateurs de ce projet."

    def has_object_permission(self, request, view, obj):
        contributors = obj.contributor_set.all()
        users = [contributor.user_id for contributor in contributors]
        return request.user in users


class DenyProjectAcess(BasePermission):
    message = "Vous ne faîtes pas partie des collaborateurs de ce projet."

    def has_permission(self, request, view):
        return False


class AuthorAccess(BasePermission):
    message = "Vous n'êtes pas le créateur de ce problème/commentaire."

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author_user_id
