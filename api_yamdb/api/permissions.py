from rest_framework.permissions import BasePermission, SAFE_METHODS


def is_safe_method(request):
    """Проверка на безопасность метода."""
    return request.method in SAFE_METHODS


class AdminOnlyPermission(BasePermission):
    """Доступ только администратору."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class ModeratorOnlyPermission(BasePermission):
    """Доступ только модератору."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_moderator
        )


def is_authenticated_managers(request):
    admin_permission = AdminOnlyPermission()
    moderator_permission = ModeratorOnlyPermission()
    return (
        admin_permission.has_permission(request, None) or
        moderator_permission.has_permission(request, None)
    )


class AdminOrSafeMethodPermission(AdminOnlyPermission):
    """
    Разрешает доступ всем пользователям для безопасных методов запроса,
    в остальных случаях — только администраторам.
    """
    def has_permission(self, request, view):
        return (
            is_safe_method(request)
            or super().has_permission(request, view)
        )


class IsAuthorModeratorAdminOrReadOnly(BasePermission):
    """
    Операции на чтение разрешены всем, остальные - автору текста,
    администратору или модератору.
    """

    def has_permission(self, request, view):
        if is_safe_method(request):
            return True
        return (
            request.user.is_authenticated
            or is_authenticated_managers(request)
        )

    def has_object_permission(self, request, view, obj):
        if is_safe_method(request):
            return True
        return (
            obj.author == request.user
            or is_authenticated_managers(request)
        )
