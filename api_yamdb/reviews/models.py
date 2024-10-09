from datetime import datetime as dt

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

import reviews.constants as const
from .utilits import calculate_max_length
from .validators import validate_creation_year, validate_username_chars


class NameSlugModel(models.Model):
    """
    Абстрактная модель с полями названия и слага.
    Умолчательная сортировка по полю названия.
    Представление объекта класса тоже по полю названия.
    """

    name = models.CharField(
        max_length=const.MAX_CONTENT_NAME,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=const.MAX_CONTENT_SLUG,
        unique=True,
        verbose_name='Идентификатор'
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:10]


class Category(NameSlugModel):
    """Модель категорий."""

    class Meta(NameSlugModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlugModel):
    """Модель жанров."""

    class Meta(NameSlugModel.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведений. Умолчательная сортировка по категории и имени."""

    name = models.CharField(
        max_length=const.MAX_CONTENT_NAME,
        verbose_name='Название'
    )
    year = models.IntegerField(
        verbose_name='Год создания',
        validators=(validate_creation_year,)
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
    )
    description = models.TextField(verbose_name='Описание', null=True)

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('category', 'name')
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'category'),
                name='unique_name_category'
            )
        ]

    def __str__(self):
        return self.name[:20]

    def get_current_year(self):
        return dt.today().year


class User(AbstractUser):
    """
    Модель пользователя с дополнительными полями:
    роль, биография, код подтверждения.
    Расширяет стандартную модель Django пользователя.
    """

    username = models.CharField(
        verbose_name='Пользователь',
        unique=True,
        max_length=const.MAX_LENGTH_USERNAME,
        validators=[
            RegexValidator(
                regex=const.USERNAME_REGEX,
                message=const.USER_NAME_INVALID_MSG,
            ),
            validate_username_chars,
        ],
    )
    email = models.EmailField(
        verbose_name='Почта',
        max_length=const.MAX_LENGTH_EMAIL,
        unique=True,
    )
    bio = models.CharField(
        verbose_name='Биография',
        max_length=const.MAX_LENGTH_BIO,
        null=True,
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=calculate_max_length(const.ROLE_CHOICES),
        choices=const.ROLE_CHOICES,
        default=const.USER,
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=const.MAX_LENGTH_CONFIRMATION_CODE,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username} ({self.email})'

    @property
    def is_admin(self):
        return (
                self.is_superuser
                or self.role == const.ADMIN
                or self.is_staff
        )

    @property
    def is_moderator(self):
        return self.role == const.MODERATOR


class TextAuthorPubdateModel(models.Model):
    """
    Абстрактная модель для наследования
    моделей взаимодействия пользователей с ресурсами.
    Поля текста, автора, даты публикации,
    умолчательная сортировка по дате публикации.
    """
    text = models.TextField(
        verbose_name='Текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='%(class)s'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)


class Review(TextAuthorPubdateModel):
    """Модель отзыва для произведения."""

    score = models.PositiveIntegerField(
        verbose_name='Оценка пользователя',
        choices=[(i, str(i)) for i in range(
            const.MIN_SCORE, const.MAX_SCORE + 1
        )],
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='%(class)s',
        verbose_name='Произведение'
    )

    def __str__(self):
        return f'Отзыв на {self.title.name[:20]} от {self.author.username}'

    class Meta(TextAuthorPubdateModel.Meta):
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review_per_title_per_user'
            )
        ]


class Comment(TextAuthorPubdateModel):
    """Модель комментария к отзыву."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        related_name='%(class)s',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='%(class)s',
        verbose_name='Произведение'
    )

    def __str__(self):
        return f'Комментарий {self.text[:20]} к отзыву {self.review.text[:20]}'

    class Meta(TextAuthorPubdateModel.Meta):
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
