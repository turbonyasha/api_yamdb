import re
from datetime import datetime as dt

from django.core.exceptions import ValidationError
from rest_framework import serializers

import reviews.constants as reviewconst
import api.constants as apiconst


def validate_username_chars(username):
    """
    Проверяет, есть ли в имени пользователя
    недопустимые символы.
    """
    if username == apiconst.USERNAME_ME:
        raise ValidationError(reviewconst.USER_REGISTER_NAME_ERROR)
    invalid_chars = set(re.sub(reviewconst.USERNAME_REGEX, '', username))
    if invalid_chars:
        raise ValidationError(
            f'Поле username содержит недопустимые символы: {invalid_chars}'
        )
    return username


def validate_creation_year(creation_year):
    this_year = dt.today().year
    if creation_year > this_year:
        raise serializers.ValidationError(
            reviewconst.VALIDATE_YEAR_ERROR.format(this_year=this_year)
        )
    return creation_year


def validate_score_1_to_10(value):
    if not (1 <= value <= 10):
        raise serializers.ValidationError(reviewconst.REVIEW_SCORE_ERROR)
    return value
