MAX_LENGTH_BIO = 254
MAX_LENGTH_EMAIL = 254
MAX_LENGTH_USERNAME = 150
MAX_LENGTH_UUID = 36
MAX_CONTENT_NAME = 256
MAX_CONTENT_SLUG = 50
MIN_SCORE = 1
MAX_SCORE = 10

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
ROLE_CHOICES = [
    (USER, 'Пользователь'),
    (ADMIN, 'Администратор'),
    (MODERATOR, 'Модератор'),
]

USER_NAME_INVALID_MSG = (
    'Поле \'username\' может содержать только буквы, цифры '
    'и символы @, ., +, -, _'
)
USERNAME_REGEX = r'^[\w.@+-]+\Z'

VALIDATE_YEAR_ERROR = (
    'Произведение не может быть создано'
    'позднее {this_year} года.'
)

USER_REGISTER_NAME_ERROR = (
    'Недопустимое имя пользователя, придумай что-нибудь еще.'
)
