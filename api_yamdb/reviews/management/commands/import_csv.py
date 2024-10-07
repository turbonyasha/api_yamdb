import csv

from django.core.management.base import BaseCommand
from django.db import models
from django.shortcuts import get_object_or_404

from reviews.models import (  # noqa
    Category, Genre, Title, User, Review, Comment
)

IMPORT_FILES_AND_MODELS = (
    # ('static/data/category.csv', Category),
    # ('static/data/genre.csv', Genre),
    ('static/data/titles.csv', Title),
    # ('static/data/genre_title.csv', GenreTitle),
    # ('static/data/users.csv', User),
    # ('static/data/review.csv', Review),
    # ('static/data/comments.csv', Comment),
)


class Command(BaseCommand):
    help = 'Импорт данных из CSV-файлов.'

    def get_row_import_data(self, headers, row, model):
        data = {}
        for header in headers:
            field = model._meta.get_field(header)
            if header[-3:] == '_id':
                data_header = header[:-3]
            else:
                data_header = header
            if isinstance(field, models.ForeignKey):
                related_model = field.related_model
                related_object = get_object_or_404(
                    related_model, pk=int(row[headers.index(header)])
                )
                if isinstance(related_object, Review):
                    data['title'] = get_object_or_404(
                        Title, pk=related_object.title_id
                    )
                data[data_header] = related_object
            else:
                data[header] = row[headers.index(field.name)]
        return data

    def handle(self, *args, **options):
        for path, model in IMPORT_FILES_AND_MODELS:
            with open(path, 'r') as csv_file:
                reader = csv.reader(csv_file)
                headers = next(reader)
                for row in reader:
                    data = self.get_row_import_data(headers, row, model)
                    if data:
                        model.objects.get_or_create(**data, defaults=data)
                        self.stdout.write(
                            f'Запись {row} в {model} залита.'
                        )
            self.stdout.write(
                self.style.SUCCESS(f'Данные модели {model} загружены.')
            )
