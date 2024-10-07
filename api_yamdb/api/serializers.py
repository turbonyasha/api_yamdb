from datetime import datetime as dt

from rest_framework import serializers
from django.core.validators import RegexValidator

import reviews.constants as cs
from reviews.models import (
    Category, Comment, Genre, Review, Title, User
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
        max_length=cs.MAX_LENGTH_USERNAME,
        validators=[
            RegexValidator(
                regex=cs.USERNAME_REGEX,
                message=cs.USER_NAME_INVALID_MSG,
            ),
        ],
        required=True,
    )
    email = serializers.EmailField(
        max_length=cs.MAX_LENGTH_EMAIL,
        required=True,
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('role',)


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
        fields = '__all__'
        read_only_fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('title', 'review')


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
                cs.VALIDATE_YEAR_ERROR
            )
        return creation_year

    def to_representation(self, title):
        representation = super().to_representation(title)
        representation['category'] = CategorySerializer(title.category).data
        representation['genre'] = GenreSerializer(
            title.genre.all(), many=True
        ).data
        return representation
