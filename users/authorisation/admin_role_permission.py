from rest_framework import permissions

from users import constants


class AdminUserOnly(permissions.BasePermission):
    """
    This is to check if the user is authenticated and is also an admin
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == constants.USER_ROLE_ADMIN:
            return True
        return False
