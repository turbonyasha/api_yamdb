from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError

from api_yamdb import settings
from reviews.models import User


def create_user(serializer):
    """
    Создает пользователя или возвращает None,
    если данные не уникальны.
    """
    try:
        user, created = User.objects.get_or_create(
            email=serializer.validated_data['email'],
            username=serializer.validated_data['username'],
        )
        return user
    except IntegrityError:
        return None


def send_confirmation_code(user):
    """Отправляет код подтверждения на email пользователя."""
    confirmation_code = default_token_generator.make_token(
        user
    )
    send_mail(
        subject='Самый секретный код для входа',
        message=f'Не говори никому этот '
                f'код для входа: {confirmation_code},'
                f'молю...',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
    )


def is_valid_confirmation_code(user, confirmation_code):
    """Проверяет корректность кода подтверждения."""
    return default_token_generator.check_token(
        user,
        confirmation_code
    )
