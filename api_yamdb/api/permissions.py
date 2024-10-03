from rest_framework.permissions import BasePermission, SAFE_METHODS

from reviews.constants import ADMIN, MODERATOR


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
            request.user.is_authenticated
            and (request.user.role == ADMIN or request.user.is_staff)
        )


class ReviewCommentSectionPermissions(BasePermission):
    """
    GET - без токена,
    POST - аутентифицированному юзеру,
    PATCH/DELETE - автору или админсоставу.
    """
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method == 'POST':
            return request.user.is_authenticated
        if request.method in ['PATCH', 'DELETE']:
            return (
                request.user.is_authenticated and (
                    request.user.role == ADMIN
                    or request.user.role == MODERATOR
                    or (hasattr(view, 'get_object')
                        and view.get_object().author == request.user)
                )
            )
