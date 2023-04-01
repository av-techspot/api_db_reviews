from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import CHAR_LIMITS_REVIEW, UserRoles


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
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    score = models.IntegerField(
        default=1,
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'

    def __str__(self) -> str:
        return f'Обзор на {self.title.name}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Обзор'
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

    def __str__(self):
        return f'Коментарий к {self.review.text[:CHAR_LIMITS_REVIEW]}'


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256)

    year = models.IntegerField(verbose_name='Год')

    description = models.TextField(verbose_name='Описание', blank=True)

    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_DEFAULT,
        related_name='titles',
        default='not_chosen',
        verbose_name='Категория')

    genre = models.ManyToManyField(
        'Genre',
        through='TitleGenre',
        verbose_name='Жанр')

    class Meta:
        ordering = ('id', )
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    @property
    def average_rating(self) -> int:
        rating = self.reviews.all().aggregate(
            models.Avg('score')).get('score__avg')
        return round(rating) if rating else None

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
        verbose_name='Произведение')
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр')

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведений'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_title_genre'
            )
        ]

    def __str__(self) -> str:
        return f'{self.title.name}: {self.genre.name}'
