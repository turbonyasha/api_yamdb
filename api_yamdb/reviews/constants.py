MAX_LENGTH_EMAIL = 254
MAX_LENGTH_USERNAME = 150
MAX_CONTENT_NAME = 256
MAX_CONTENT_SLUG = 50
MIN_SCORE = 1
MAX_SCORE = 10
USERNAME_REGEX = r'^[\w.@+-]+\Z'
ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
USER_NAME_INVALID_MSG = (
    'Поле username может содержать только буквы, цифры '
    'и символы @, ., +, -, _'
)
VALIDATE_YEAR_ERROR = (
    'Произведение не может быть создано'
    'позднее текущего года ({this_year}). '
    'Вы ввели: {imput_year}'
)
USER_REGISTER_NAME_ERROR = (
    'Недопустимое имя пользователя.'
)
VALIDATE_ERROR_USERNAME_ME = 'Имя me недопустимо.'
