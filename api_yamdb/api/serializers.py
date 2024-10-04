
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, User

from django.core.validators import RegexValidator
from rest_framework import serializers

from reviews.constants import (
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_USERNAME,
    USER_NAME_INVALID_MSG,
    USERNAME_REGEX,
    SLUG_REGEX,
    SLUG_INVALID_MSG
)


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'bio',
            'role',
        )


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME,
        validators=[
            RegexValidator(
                regex=USERNAME_REGEX,
                message=USER_NAME_INVALID_MSG,
            ),
        ],
        required=True,
    )
    email = serializers.EmailField(
        max_length=MAX_LENGTH_EMAIL,
        required=True,
    )


class UserSerializer(AdminSerializer):
    role = serializers.StringRelatedField()


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True
    )
    confirmation_code = serializers.CharField(
        required=True
    )

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code',
        )


class CategoryGenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
        validators=[
            RegexValidator(
                regex=SLUG_REGEX,
                message=SLUG_INVALID_MSG,
            ),
        ],
    )


class CategorySerializer(CategoryGenreSerializer):

    class Meta:
        model = Category
        exclude = ['id']


class GenreSerializer(CategoryGenreSerializer):

    class Meta:
        model = Genre
        exclude = ['id']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return int(sum(
                review.score for review in reviews
            ) / len(reviews))
        else:
            return 0
