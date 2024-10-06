from datetime import datetime as dt

from rest_framework import serializers

from reviews.models import (
    Category, Comment, Genre, Review, Title, User
)

from django.core.validators import RegexValidator
from rest_framework import serializers

from reviews.constants import (
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_USERNAME,
    USER_NAME_INVALID_MSG,
    USERNAME_REGEX,
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


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ['id',]


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ['id',]


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
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_rating(self, title):
        reviews = title.reviews.all()
        if reviews:
            return int(sum(
                review.score for review in reviews
            ) / len(reviews))
        else:
            return

    def validate_year(self, creation_year):
        if creation_year > dt.today().year:
            raise serializers.ValidationError(
                'Произведение не может быть создано в будущем!'
            )
        return creation_year

    def to_representation(self, title):
        representation = super().to_representation(title)
        representation['category'] = CategorySerializer(title.category).data
        representation['genre'] = GenreSerializer(
            title.genre.all(), many=True
        ).data
        return representation
