from django.core.mail import send_mail

from api.constants import SEND_MAIL_MESSAGE
from api_yamdb import settings


def send_confirmation_code(user, confirmation_code):
    """Отправляет код подтверждения на email пользователя."""
    send_mail(
        subject='Самый секретный код для входа',
        message=SEND_MAIL_MESSAGE.format(
            confirmation_code=confirmation_code
        ),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
    )
