USERNAME_ME = 'me'
MAX_LENGTH_EMAIL = 254

SEND_MAIL_MESSAGE = (
    'Не говори никому этот код для входа: {confirmation_code}, молю...'
)
CONFIRMATION_CODE_ERROR = 'Неверный код подтверждения, товарищ.'

USER_REGISTER_ERROR = (
    'Указанный username существует! Ты нас не обманешь, мошенник.'
)
EMAIL_REGISTER_ERROR = (
    'Указанный email существует! Ты нас не обманешь, мошенник.'
)

ALLOWED_HTTP_METHODS = ('get', 'post', 'delete', 'patch')
ALLOWED_HTTP_METHODS_CATEGORY_GENRE = ('get', 'post', 'delete')
