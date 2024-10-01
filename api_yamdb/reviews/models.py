from django.db import models


class NameSlugModel(models.Model):
    """
    Абстрактная модель с полями названия и слага.
    Умолчательная сортировка по полю названия.
    Представление объекта класса тоже по полю названия.
    """

    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(NameSlugModel):
    """Модель категорий."""

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlugModel):
    """Модель жанров."""

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведений. Умолчательная сортировка по категории."""

    name = models.CharField(
        max_length=200, verbose_name='Название произведения'
    )
    year = models.IntegerField(verbose_name='Год создания')
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True,
    )
    genres = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        blank=True,
        verbose_name='Жанр'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('category',)


class GenreTitle(models.Model):
    """Промежуточная модель для произведений и жанров."""

    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)
