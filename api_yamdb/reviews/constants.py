MAX_LENGTH_EMAIL = 254
MAX_LENGTH_USERNAME = 150
MAX_CONTENT_LENGTH_NAME = 256
MAX_CONTENT_LENGTH_SLUG = 50
MIN_SCORE = 1
MAX_SCORE = 10
USERNAME_REGEX = r'^[\w.@+-]+\Z'
ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
VALIDATE_YEAR_ERROR = (
    'Произведение не может быть создано'
    'позднее текущего года ({this_year}). '
    'Вы ввели: {imput_year}'
)
USER_REGISTER_NAME_ERROR = (
    'Имя пользователя {username} недопустимо.'
)
INVALID_USERNAME_CHARS = (
    'Поле username содержит недопустимые символы: {invalid_chars}'
)
CLASS_NAME = '%(class)ss'
