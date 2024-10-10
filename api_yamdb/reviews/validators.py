import re
from datetime import datetime as dt

from django.core.exceptions import ValidationError

import reviews.constants as const


def validate_username_chars(username):
    """
    Проверяет, есть ли в имени пользователя
    недопустимые символы.
    """
    if username == const.USERNAME_ME:
        raise ValidationError(
            const.USER_REGISTER_NAME_ERROR.format(
                username=username
            )
        )
    invalid_chars = set(re.sub(const.USERNAME_REGEX, '', username))
    if invalid_chars:
        repr_chars = list(map(repr, sorted(invalid_chars)))
        invalid_chars_str = ', '.join(repr_chars)
        raise ValidationError(
            const.INVALID_USERNAME_CHARS.format(
                invalid_chars=invalid_chars
            )
        )
    return username


def validate_creation_year(creation_year):
    this_year = dt.today().year
    if creation_year > this_year:
        raise ValidationError(
            const.VALIDATE_YEAR_ERROR.format(
                this_year=this_year, input_year=creation_year
            )
        )
    return creation_year


def validate_score(score):
    if not (const.MIN_SCORE <= score <= const.MAX_SCORE):
        raise ValidationError(
            const.REVIEW_SCORE_ERROR.format(
                score=score,
                min=const.MIN_SCORE,
                max=const.MAX_SCORE
            )
        )
    return score
