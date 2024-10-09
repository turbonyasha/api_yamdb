from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminPermission(BasePermission):
    """
    Разрешает доступ всем пользователям для безопасных методов запроса,
    в остальных случаях — только администраторам.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin
            )
        )


class AdminOnlyPermission(BasePermission):
    """Доступ только администратору."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAuthorAdminOrReadOnly(BasePermission):
    """
    Операции на чтение разрешены всем, остальные - автору текста,
    администратору или модератору.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return AdminOnlyPermission() or request.user.is_moderator
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (
            obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )
