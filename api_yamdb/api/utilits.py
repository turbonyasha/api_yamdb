import re

from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from api.constants import SEND_MAIL_MESSAGE
from api_yamdb import settings
import reviews.constants as cs


def send_confirmation_code(user):
    """Отправляет код подтверждения на email пользователя."""
    confirmation_code = default_token_generator.make_token(
        user
    )
    send_mail(
        subject='Самый секретный код для входа',
        message=SEND_MAIL_MESSAGE.format(
            confirmation_code=confirmation_code
        ),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
    )


def validate_username_chars(username):
    """
    Проверяет, есть ли в имени пользователя
    недопустимые символы.
    """

    if username.lower() == 'me':
        raise ValidationError(
            f'Имя \'{username}\' недопустимо. '
            f'Придумайте другое.'
        )

    invalid_chars = []
    for char in username:
        if not re.match(cs.USERNAME_REGEX, char):
            invalid_chars.append(char)

    if invalid_chars:
        invalid_chars_list = ', '.join(
            set(invalid_chars)
        )
        raise ValidationError(
            f'Поле \'username\' содержит '
            f'недопустимые символы: \'{invalid_chars_list}\'.'
        )
