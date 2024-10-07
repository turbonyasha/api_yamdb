def calculate_max_length(choices):
    """
    Функция для вычисления максимальной длины строк в списке choices.
    """
    return max(len(choice[0]) for choice in choices)
