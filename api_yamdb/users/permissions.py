from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    """Разрешение на запросы только админу."""

    def has_permission(self, request, view):
        return (
            request.user.role == 'admin'
            or request.user.is_staff
        )
