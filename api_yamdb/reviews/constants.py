MAX_LENGTH_EMAIL = 254
MAX_LENGTH_USERNAME = 150
MAX_LENGTH_NAME = 256
MAX_LENGTH_SLUG = 50
MIN_SCORE = 1
MAX_SCORE = 10
USERNAME_REGEX = r'^[\w.@+-]+\Z'
ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
PROFILE_URL_NAME = 'me'
VALIDATE_YEAR_ERROR = (
    'Произведение не может быть создано в {imput_year} году, '
    'это позднее текущего года: {this_year}. '
)
USER_REGISTER_NAME_ERROR = (
    'Имя пользователя {username} недопустимо.'
)
INVALID_USERNAME_CHARS = (
    'Поле username содержит недопустимые символы: {invalid_chars}'
)
REVIEW_SCORE_ERROR = (
    'Оценка не может иметь значение {score}, '
    'допустимые значения от {min} до {max}.'
)
