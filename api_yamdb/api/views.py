from api.utilits import (
    create_user,
    is_valid_confirmation_code,
    send_confirmation_code
)
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    exceptions,
    filters,
    permissions,
    status,
    viewsets
)
from rest_framework.decorators import (
    action,
    api_view,
    permission_classes
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

import reviews.constants as cs
from reviews.models import User, Category, Genre, Title, Review
from .filters import TitleFilter
from .permissions import (
    AdminOnlyPermission,
    ReviewCommentSectionPermissions,
    AdminUserPermission
)
from .serializers import (
    AdminSerializer,
    AuthSerializer,
    GetTokenSerializer,
    UserSerializer,
    GenreSerializer,
    TitleSerializer,
    CategorySerializer,
    ReviewSerializer,
    CommentSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    Представление для реализации операций для
    кастомной модели пользователя.
    """
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (AdminOnlyPermission,)
    http_method_names = [
        'get',
        'post',
        'delete',
        'patch',
    ]

    @action(
        methods=['GET', 'PATCH'],
        url_path='me',
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def profile(self, request):
        """Получение/обновление данных пользователя."""
        if request.method == 'GET':
            return self.get_user_data(request)

        if request.method == 'PATCH':
            return self.update_user_data(request)

    def get_user_data(self, request) -> Response:
        """Получение данных текущего пользователя."""
        serializer = UserSerializer(request.user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def update_user_data(self, request) -> Response:
        """Обновление данных пользователя."""
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(
            raise_exception=True
        )
        serializer.save(
            role=request.user.role
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny],)
def register_user(request):
    """Регистрации нового пользователя."""
    serializer = AuthSerializer(
        data=request.data
    )
    serializer.is_valid(
        raise_exception=True
    )
    user = create_user(serializer)
    if not user:
        return Response(
            {
                'error': cs.USER_REGISTER_ERROR
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if user.username == 'me':
        return Response(
            {
                'error': cs.USER_REGISTER_NAME_ERROR
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    send_confirmation_code(user)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([permissions.AllowAny], )
def get_user_token(request):
    """Получения токена пользователя."""
    serializer = GetTokenSerializer(
        data=request.data
    )
    serializer.is_valid(
        raise_exception=True
    )

    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )

    if not is_valid_confirmation_code(
            user,
            serializer.validated_data['confirmation_code']
    ):
        return Response(
            {
                'error': cs.CONFIRMATION_CODE_ERROR
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(
        {
            'token': str(AccessToken.for_user(user))
        },
        status=status.HTTP_200_OK
    )


class CategoryGenreViewSet(viewsets.ModelViewSet):
    """Представление для работы с категориями и жанрами."""
    permission_classes = (AdminUserPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(CategoryGenreViewSet):
    """Представление для работы только с жанрами."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(CategoryGenreViewSet):
    """Представление для работы только с категориями."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Представление для работы с произведениями."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AdminUserPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT' or not request.user.role == cs.ADMIN:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return super().update(request, *args, **kwargs)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Представление для реализации операций
    для модели отзывов на произведени.
    """
    serializer_class = ReviewSerializer
    permission_classes = [ReviewCommentSectionPermissions]

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        if Review.objects.filter(
            title_id=self.kwargs.get('title_id'),
            author=self.request.user
        ).exists():
            raise exceptions.ValidationError(
                "Вы уже оставили отзыв на это произведение."
            )
        serializer.save(author=self.request.user, title=self.get_title())

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return super().update(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Представление для реализации операций
    для модели комментариев к отзывам на произведения.
    """
    serializer_class = CommentSerializer
    permission_classes = [ReviewCommentSectionPermissions]

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs['review_id'])

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(
            author=self.request.user,
            review=review,
            title=review.title)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return super().update(request, *args, **kwargs)
