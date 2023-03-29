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


class Review(models.Model):
    title = models.ForeignKey(
        Title,
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
        default=1
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
        return self.title


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Ревью',
        related_name='reviews'
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
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
