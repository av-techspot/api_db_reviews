from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import UserRoles
from api_yamdb.settings import DISPLAY_TEXT_LIMIT


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Email-адрес',
        max_length=254,
        blank=False,
        unique=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=25,
        choices=UserRoles.choices,
        default=UserRoles.USER,
    )

    class Meta:
        ordering = ('id', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Review(models.Model):
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        verbose_name='Название произведения',
        related_name='titles'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    score = models.IntegerField(
        models.SET_DEFAULT,
        default=1,
        verbose_name='Рейтинг'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'

    def __str__(self) -> str:
        return self.text[:DISPLAY_TEXT_LIMIT]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Ревью'
    )
    text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('pub_date',)
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return self.text[:DISPLAY_TEXT_LIMIT]


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256)

    year = models.IntegerField(verbose_name='Год')

    description = models.TextField(verbose_name='Описание')

    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_DEFAULT,
        related_name='titles',
        default='not_chosen',
        verbose_name='Категория')

    class Meta:
        ordering = ('id', )
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    @property
    def average_rating(self) -> int:
        rating = self.reviews.all().aggregate(models.Avg('score'))
        return round(rating['score__avg'])

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название')

    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг')

    class Meta:
        ordering = ('id', )
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название')

    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг')

    class Meta:
        ordering = ('id', )
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genres',
        verbose_name='Произведение')
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Жанр')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_title_genre'
            )
        ]
