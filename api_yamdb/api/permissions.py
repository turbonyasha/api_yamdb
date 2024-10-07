from rest_framework.permissions import BasePermission, SAFE_METHODS

from rest_framework.response import Response
from rest_framework import status


class AdminPermission(BasePermission):
    """
    Разрешает доступ всем пользователям для безопасных методов запроса,
    в остальных случаях — только администраторам.
    """

    def has_permission(self, request, view):
        return (
                request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin)
        )


class AdminOnlyPermission(BasePermission):
    """Доступ только администратору."""

    def has_permission(self, request, view):
        return (
                request.user.is_authenticated
                and request.user.is_admin
        )


class ReviewCommentSectionPermissions(BasePermission):
    """
    GET - без токена,
    POST - аутентифицированному юзеру,
    PATCH/DELETE - автору или админсоставу,
    PUT - запрещен.
    """
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method == 'POST':
            return request.user.is_authenticated
        if request.method in ['PATCH', 'DELETE']:
            return (
                request.user.is_authenticated and (
                    request.user.is_admin
                    or request.user.is_moderator
                    or (hasattr(view, 'get_object')
                        and view.get_object().author == request.user)
                )
            )
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
