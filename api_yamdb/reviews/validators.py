import re
from datetime import datetime as dt

from django.core.exceptions import ValidationError
from rest_framework import serializers

import reviews.constants as const


def validate_username_chars(username):
    """
    Проверяет, есть ли в имени пользователя
    недопустимые символы.
    """

    if username.lower() == 'me':
        raise ValidationError(
            f'Имя \'{username}\' недопустимо. '
            f'Придумайте другое.'
        )

    invalid_chars = []
    for char in username:
        if not re.match(const.USERNAME_REGEX, char):
            invalid_chars.append(char)

    if invalid_chars:
        invalid_chars_list = ', '.join(
            set(invalid_chars)
        )
        raise ValidationError(
            f'Поле \'username\' содержит '
            f'недопустимые символы: \'{invalid_chars_list}\'.'
        )
    return username


def validate_creation_year(creation_year):
    this_year = dt.today().year
    if creation_year > this_year:
        raise serializers.ValidationError(
            const.VALIDATE_YEAR_ERROR.format(this_year=this_year)
        )
    return creation_year


def validate_score_1_to_10(value):
    if not (1 <= value <= 10):
        raise serializers.ValidationError(const.REVIEW_SCORE_ERROR)
    return value
