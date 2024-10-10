from rest_framework import serializers, exceptions

from .constants import REVIEW_VALIDATE_ERROR
import reviews.constants as const
from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import (
    validate_creation_year, validate_username_chars, validate_score
)


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
        validators=[validate_username_chars],
        required=True,
    )
    email = serializers.EmailField(
        max_length=const.MAX_LENGTH_EMAIL,
        required=True,
    )


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=const.MAX_LENGTH_USERNAME,
        required=True,
        validators=[validate_username_chars]
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

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date'
        )

    def validate_score(self, score):
        return validate_score(score)

    def validate(self, data):
        if Review.objects.filter(
                title_id=self.context['view'].kwargs['title_id'],
                author=self.context['request'].user
        ).exists() and self.context['request'].method == 'POST':
            raise exceptions.ValidationError(REVIEW_VALIDATE_ERROR)
        return data


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, )
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
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

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date'
        )
