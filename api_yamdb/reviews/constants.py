MAX_LENGTH_BIO = 254
MAX_LENGTH_EMAIL = 254
MAX_LENGTH_NAME = 154
MAX_LENGTH_USERNAME = 150
MAX_LENGTH_ROLE = 10
MAX_LENGTH_UUID = 36
MAX_CONTENT_NAME = 256
MAX_CONTENT_SLUG = 50

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]

USER_NAME_INVALID_MSG = (
    'Поле \'username\' может содержать только буквы и цифры.'
)
USERNAME_REGEX = r'^[\w.@+-]+\Z'

SLUG_REGEX = r'^[-a-zA-Z0-9_]+$'
SLUG_INVALID_MSG = (
    'Поле \'slug\' может содержать только буквы, цифры, дефис и подчеркивание.'
)
