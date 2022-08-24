from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Genre(models.Model):
    """Модель жанра произведения."""

    name = models.CharField('Название жанра', max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('slug',)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель категории произведения."""

    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('slug',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField('Название произведения', max_length=200)
    year = models.PositiveSmallIntegerField('Год издания произведения')
    description = models.TextField(
        'Описание произведения',
        blank=True, null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        null=True
    )

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель для связи произведений и жанров."""

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}: {self.genre}'


class Review(models.Model):
    """Модель для отзывов к произведению."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    text = models.TextField('Текст отзыва', max_length=2000, blank=True)
    score = models.PositiveSmallIntegerField(
        'Оценка',
        choices=zip(range(0, 11), range(0, 11),),
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='cant_review_twice'
            )
        ]

    def __str__(self):
        return f'{self.title}: {self.text[:15]}'


class Comments(models.Model):
    """Модель для комментариев к отзыву."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    text = models.TextField('Текст комментария', max_length=500)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.review}: {self.text[:15]}'
