import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from reviews.constants import (
    MAX_LENGTH_BIO,
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_NAME,
    MAX_LENGTH_USERNAME,
    ROLE_CHOICES,
    USER, MAX_LENGTH_ROLE,
)


class User(AbstractUser):
    """Дополнительные поля к базовой модели auth_user."""

    username = models.CharField(
        verbose_name='Пользователь',
        unique=True,
        max_length=MAX_LENGTH_USERNAME,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Поле \'username\' может содержать только буквы и цифры.'
            ),
        ],
    )
    email = models.EmailField(
        verbose_name='email',
        unique=True,
        max_length=MAX_LENGTH_EMAIL,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=MAX_LENGTH_NAME,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=MAX_LENGTH_NAME,
    )
    bio = models.CharField(
        verbose_name='Био',
        max_length=MAX_LENGTH_BIO,
        null=True,
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=ROLE_CHOICES,
        default=USER,
        max_length=MAX_LENGTH_ROLE,
    )
    confirmation_code = models.CharField(
        verbose_name='Самый секретный код',
        default=uuid.uuid4,
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
