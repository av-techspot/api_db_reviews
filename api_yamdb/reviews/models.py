from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import UserRoles


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


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        blank=True,
        max_length=256)

    year = models.IntegerField(
        verbose_name='Год',
        blank=True)

    description = models.TextField(verbose_name='Описание')

    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_DEFAULT,
        related_name='titles',
        blank=True,
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
        blank=True,
        max_length=256,
        verbose_name='Название')

    slug = models.SlugField(
        blank=True,
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
        blank=True,
        max_length=256,
        verbose_name='Название')

    slug = models.SlugField(
        blank=True,
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
