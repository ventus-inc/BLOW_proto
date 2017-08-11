from rest_framework import permissions

# permissions.py
class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """

    def has_object_permission(self, request, view, obj=None):
        return obj.from_user == request.user
