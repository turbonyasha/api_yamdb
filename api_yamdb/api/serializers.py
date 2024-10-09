from django.core.validators import RegexValidator
from rest_framework import serializers, exceptions

import reviews.constants as const
from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import (
    validate_creation_year, validate_username_chars, validate_score_1_to_10
)


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

    def validate_username(self, username):
        return validate_username_chars(username)


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

    def validate_score(self, score):
        return validate_score_1_to_10(score)

    def validate(self, data):
        if Review.objects.filter(
            title_id=self.context['view'].kwargs['title_id'],
            author=self.context['request'].user
        ).exists() and self.context['request'].method == 'POST':
            raise exceptions.ValidationError(
                'Вы уже оставили отзыв на это произведение.'
            )
        return data


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True,)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        read_only_fields = fields


class TitleCRUDSerializer(TitleReadSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta(TitleReadSerializer.Meta):
        read_only_fields = ()

    def validate_year(self, creation_year):
        return validate_creation_year(creation_year)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = TitleReadSerializer(read_only=True)
    review = ReviewSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'