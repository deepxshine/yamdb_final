from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField('Slug жанра', max_length=50, unique=True)

    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.slug


class Category(models.Model):
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField('Slug категории', max_length=50, unique=True)

    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=256)
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание', null=True, blank=True)
    genre = models.ManyToManyField(
        to=Genre,
        related_name='titles'
    )
    category = models.ForeignKey(
        to=Category,
        related_name='category',
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['year']),
            # models.Index(fields=['genre']),
            models.Index(fields=['category'])
        ]

    def __str__(self):
        return self.name[:50]


class Review(models.Model):
    text = models.TextField('Текст ревью')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField('Рейтинг', validators=[
        MaxValueValidator(10), MinValueValidator(1)])
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='Unique review'
            )
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True)
