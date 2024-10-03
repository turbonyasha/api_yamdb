from rest_framework.permissions import BasePermission, SAFE_METHODS

from reviews.constants import ADMIN


class AdminUserPermission(BasePermission):
    """
    Разрешает доступ всем пользователям для безопасных методов запроса,
    в остальных случаях — только администраторам.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (request.user.is_authenticated
                and request.user.role == ADMIN)
        )


class AdminOnlyPermission(BasePermission):
    """Доступ только администратору."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (request.user.role == ADMIN or request.user.is_staff)
        )
