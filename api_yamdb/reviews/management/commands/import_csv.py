import csv

from django.core.management.base import BaseCommand
from django.db import models
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Title, User, Review, Comment
from api_yamdb.settings import STATICFILES_DIRS

FILES_DIR = STATICFILES_DIRS[0].as_posix() + '/data/'


# Сообщения скрипта

HELP = 'Импорт данных из CSV-файлов для учебного проекта API_YamDB.'
ROW_SUCCESS = 'Запись {row} в {model} залита.'
MANY_TO_MANY_SUCCESS = ('Связь между произведением "{title}" '
                        'и жанром "{genre}" загружена.')
MODEL_SUCCESS = 'Данные модели {model} загружены.'
FILE_NOT_FOUND = 'Файл {path} для модели {model} не найден.'


# Адреса файлов и модели для загрузки

IMPORT_FILES_AND_MODELS = (
    (FILES_DIR + 'category.csv', Category),
    (FILES_DIR + 'genre.csv', Genre),
    (FILES_DIR + 'titles.csv', Title),
    (FILES_DIR + 'users.csv', User),
    (FILES_DIR + 'review.csv', Review),
    (FILES_DIR + 'comments.csv', Comment),
    (FILES_DIR + 'genre_title.csv', None),
)


class Command(BaseCommand):
    help = HELP

    def get_row_import_data(self, headers, row, model):
        data = {}
        for header in headers:
            field = model._meta.get_field(header)
            if header.endswith('_id'):
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

    def title_genre_handle(self, path):
        with open(path, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            headers = next(reader)
            for row in reader:
                title = get_object_or_404(
                    Title, pk=int(row[headers.index('title_id')])
                )
                genre = get_object_or_404(
                    Genre, pk=int(row[headers.index('genre_id')])
                )
                title.genre.add(genre)
                self.stdout.write(MANY_TO_MANY_SUCCESS.format(
                    title=title.name, genre=genre.name
                ))
        self.stdout.write(
            self.style.SUCCESS(MODEL_SUCCESS.format(model='GenreTitle'))
        )

    def handle(self, *args, **options):
        for path, model in IMPORT_FILES_AND_MODELS:
            try:
                if not model:
                    self.title_genre_handle(path)
                    continue
                with open(path, 'r', encoding='utf-8') as csv_file:
                    reader = csv.reader(csv_file)
                    headers = next(reader)
                    for row in reader:
                        data = self.get_row_import_data(headers, row, model)
                        if data:
                            model.objects.get_or_create(**data, defaults=data)
                            self.stdout.write(ROW_SUCCESS.format(
                                row=row, model=model.__name__
                            ))
                self.stdout.write(self.style.SUCCESS(
                    MODEL_SUCCESS.format(model=model.__name__)
                ))
            except FileNotFoundError:
                self.stdout.write(self.style.ERROR(
                    FILE_NOT_FOUND.format(path=path, model=model.__name__)
                ))
