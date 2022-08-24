from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Разрешение на просмотр всем и на изменение админу."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == 'admin'
            or request.user.is_staff
        )


class IsAuthorModAdmOrReadOnly(permissions.BasePermission):
    """
    Разрешение на просмотр всем и на изменение автору, модератору или админу.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role in ('admin', 'moderator')
            or request.user.is_staff
        )
