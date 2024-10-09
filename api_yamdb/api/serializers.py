from django.db import IntegrityError
from django.core.validators import RegexValidator
from rest_framework import serializers

import reviews.constants as const
from api.utilits import validate_username_chars
from reviews.models import Category, Comment, Genre, Review, Title, User


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('role',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=const.MAX_LENGTH_USERNAME,
        validators=[
            RegexValidator(
                regex=const.USERNAME_REGEX,
                message=const.USER_NAME_INVALID_MSG,
            ),
        ],
        required=True,
    )
    email = serializers.EmailField(
        max_length=const.MAX_LENGTH_EMAIL,
        required=True,
    )

    def validate_username(self, value):
        validate_username_chars(value)
        return value


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=const.MAX_LENGTH_USERNAME,
        required=True
    )
    confirmation_code = serializers.CharField(
        required=True
    )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = serializers.SlugRelatedField(
        read_only=True, slug_field='name'
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate_score(self, value):
        if not (1 <= value <= 10):
            raise serializers.ValidationError(const.REVIEW_SCORE_ERROR)
        return value

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на это произведение.'
            )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = serializers.SlugRelatedField(
        read_only=True, slug_field='name'
    )
    review = serializers.SlugRelatedField(
        read_only=True, slug_field='text'
    )

    class Meta:
        model = Comment
        fields = '__all__'


class TitleReadSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class TitleUpdateSerializer(TitleReadSerializer):
    rating = serializers.FloatField(read_only=True)

    def to_representation(self, title):
        representation = super().to_representation(title)
        representation['category'] = CategorySerializer(title.category).data
        representation['genre'] = GenreSerializer(
            title.genre.all(), many=True
        ).data
        return representation
