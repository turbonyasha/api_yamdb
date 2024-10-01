import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Genre, Title, GenreTitle  # noqa


MODELS_AND_PATHS = (
    (Category, 'static/data/category.csv'),
    (Genre, 'static/data/genre.csv'),
    # (Title, 'static/data/titles.csv'),
    # (GenreTitle, 'static/data/genre_title.csv'),
)


class Command(BaseCommand):
    help = 'Импорт данных из CSV-файлов.'

    def handle(self, *args, **options):
        for model, path in MODELS_AND_PATHS:
            with open(path, 'r') as csv_file:
                reader = csv.reader(csv_file)
                header = next(reader)
                for row in reader:
                    model.objects.get_or_create(
                        name=row[header.index('name')],
                        slug=row[header.index('slug')],
                    )
            self.stdout.write(self.style.SUCCESS('Данные импортированы'))
