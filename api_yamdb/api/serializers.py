from datetime import datetime as dt

# from django.shortcuts import get_object_or_404
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
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
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

    def validate_year(self, creation_year):
        year = dt.today().year
        if creation_year > year:
            raise serializers.ValidationError(
                'Произведение не может быть создано в будущем!'
            )
        return creation_year

    # def validate_genre(self, category):
    #     return get_object_or_404(Category, slug=category)

    # def validate_category(self, genres):
    #     all_genres = [
    #         get_object_or_404(Category, slug=genre) for genre in genres
    #     ]
    #     return all_genres

    # def create(self, validated_data):
    #     genres = self.initial_data['genre']
    #     category = get_object_or_404(
    #         Category, slug=self.initial_data['category']
    #     )
    #     checked = []
    #     for genre in genres:
    #         cur_genre = get_object_or_404(Genre, slug=genre)
    #         checked.append(cur_genre)
    #     validated_data['category'] = category
    #     validated_data['genre'] = checked
    #     return Title.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.year = validated_data.get('year', instance.year)
    #     instance.category = validated_data.get('category', instance.category)
    #     instance.description = validated_data.get(
    #         'description', instance.description
    #     )
    #     genres_data = validated_data.pop('genre')
    #     lst = []
    #     for genre in genres_data:
    #         current_genre, _ = Genre.objects.get_or_create(**genre)
    #         lst.append(current_genre)
    #     instance.achievements.set(lst)

    #     instance.save()
    #     return instance
