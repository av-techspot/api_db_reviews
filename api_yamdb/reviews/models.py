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
