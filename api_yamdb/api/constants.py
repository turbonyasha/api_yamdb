ALLOWED_HTTP_METHODS = ('get', 'post', 'delete', 'patch')
ALLOWED_HTTP_METHODS_CATEGORY_GENRE = ('get', 'post', 'delete')

SEND_MAIL_MESSAGE = (
    'Код подтверждения: {confirmation_code}'
)
CONFIRMATION_CODE_ERROR = 'Неверный код подтверждения.'
USER_REGISTER_ERROR = (
    'Этот username уже существует.'
)
EMAIL_REGISTER_ERROR = (
    'Этот email уже существует.'
)
REVIEW_VALIDATE_ERROR = 'Вы уже оставили отзыв на это произведение.'
