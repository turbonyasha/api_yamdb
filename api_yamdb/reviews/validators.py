from datetime import datetime as dt

from rest_framework import serializers

from .constants import VALIDATE_YEAR_ERROR


def validate_creation_year(creation_year):
    this_year = dt.today().year
    if creation_year > this_year:
        raise serializers.ValidationError(
            VALIDATE_YEAR_ERROR.format(this_year=this_year)
        )
    return creation_year
