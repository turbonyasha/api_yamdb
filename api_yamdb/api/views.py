
from django.shortcuts import get_object_or_404
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

from api.utilits import (
    create_user,
    is_valid_confirmation_code,
    send_confirmation_code
)
from reviews.models import User, Review, Title, Comment
from .permissions import AdminOnlyPermission, ReviewCommentSectionPermissions
from .serializers import (
    AdminSerializer,
    AuthSerializer,
    GetTokenSerializer,
    UserSerializer,
    ReviewSerializer,
    CommentSerializer
)


class UserViewSet(viewsets.ModelViewSet):
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
                'error': 'Указанный username '
                         'или email существует!'
                         'Ты нас не обманешь, мошенник.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if user.username == 'me':
        return Response(
            {
                'error': 'Недопустимое имя пользователя, '
                         'придумай что-нибудь еще.'
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
                'error': 'Неверный код подтверждения, товарищ.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(
        {
            'token': str(AccessToken.for_user(user))
        },
        status=status.HTTP_200_OK
    )


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Представление для реализации операций
    GET, POST, PATCH, DELETE
    для модели отзывов.
    """
    serializer_class = ReviewSerializer
    permission_classes = [ReviewCommentSectionPermissions]

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title.reviews.all()

    def perform_create(self, serializer):
        if Review.objects.filter(
            title_id=self.kwargs.get('title_id'),
            author=self.request.user
        ).exists():
            raise exceptions.ValidationError(
                "Вы уже оставили отзыв на это произведение."
            )
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """
    Представление для реализации операций
    GET, POST, PATCH, DELETE
    для модели комментариев к отзывам.
    """
    serializer_class = CommentSerializer
    permission_classes = [ReviewCommentSectionPermissions]

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs['review_id'])

    def get_queryset(self):
        return self.get_review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
