import random

from api_yamdb import settings


def calculate_max_length(choices):
    """
    Функция для вычисления максимальной длины строк в списке choices.
    """
    return max(len(choice[0]) for choice in choices)


def generate_confirmation_code():
    """
    Генерирует код подтверждения заданной длины из допустимых символов.
    """

    return ''.join(
        random.choices(
            settings.CONFIRMATION_CODE_CHARACTERS,
            k=settings.CONFIRMATION_CODE_LENGTH
        )
    )
