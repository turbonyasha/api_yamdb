import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from reviews.constants import (
    MAX_LENGTH_BIO,
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_ROLE,
    MAX_LENGTH_ROLE,
    MAX_LENGTH_USERNAME,
    MAX_LENGTH_UUID,
    MAX_LENGTH_UUID,
    MAX_CONTENT_NAME,
    MAX_CONTENT_SLUG,
    ROLE_CHOICES,
    USER,
    USER_NAME_INVALID_MSG,
    USERNAME_REGEX,
)


class NameSlugModel(models.Model):
    """
    Абстрактная модель с полями названия и слага.
    Умолчательная сортировка по полю названия.
    Представление объекта класса тоже по полю названия.
    """

    name = models.CharField(
        max_length=MAX_CONTENT_NAME,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=MAX_CONTENT_SLUG,
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:10]


class Category(NameSlugModel):
    """Модель категорий."""

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Genre(NameSlugModel):
    """Модель жанров."""

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)


class Title(models.Model):
    """Модель произведений. Умолчательная сортировка по категории."""

    name = models.CharField(
        max_length=MAX_CONTENT_NAME, verbose_name='Название произведения'
    )
    year = models.IntegerField(verbose_name='Год создания')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр',
    )
    description = models.TextField(verbose_name='Описание', null=True)

    def __str__(self):
        return self.name[:20]

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('category',)
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'category'],
                name='unique_name_category'
            )
        ]


class GenreTitle(models.Model):
    """Промежуточная модель для произведений и жанров."""

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class User(AbstractUser):
    """Дополнительные поля к базовой модели auth_user."""

    username = models.CharField(
        verbose_name='Пользователь',
        unique=True,
        max_length=MAX_LENGTH_USERNAME,
        validators=[
            RegexValidator(
                regex=USERNAME_REGEX,
                message=USER_NAME_INVALID_MSG,
            ),
        ],
    )
    email = models.EmailField(
        'Почта',
        max_length=MAX_LENGTH_EMAIL,
        unique=True,
    )
    bio = models.CharField(
        'Био',
        max_length=MAX_LENGTH_BIO,
        null=True,
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=MAX_LENGTH_ROLE,
        choices=ROLE_CHOICES,
        default=USER,
    )
    confirmation_code = models.CharField(
        verbose_name='Самый секретный код',
        default=uuid.uuid4,
        max_length=MAX_LENGTH_UUID,
        editable=False,
        unique=True,
        auto_created=True
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username} ({self.email})'


class Review(models.Model):
    """Модель отзыва для произведения."""

    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва'
    )
    score = models.PositiveIntegerField(
        verbose_name='Оценка пользователя',
        choices=[(i, str(i)) for i in range(1, 11)]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    def __str__(self):
        return f'Отзыв на {self.title.name} от {self.author.username}'

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        default_related_name = 'reviews'


class Comment(models.Model):
    """Модель комментария к отзыву."""

    text = models.TextField(
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return f'Комментарий к отзыву {self.review.text[:20]}'

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)
        default_related_name = 'comments'
