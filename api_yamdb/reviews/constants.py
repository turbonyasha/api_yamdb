MAX_LENGTH_BIO = 254
MAX_LENGTH_EMAIL = 254
MAX_LENGTH_NAME = 154
MAX_LENGTH_USERNAME = 150
MAX_LENGTH_ROLE = 10
MAX_LENGTH_UUID = 36

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
