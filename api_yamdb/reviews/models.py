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


class Titles(models.Model):
    name = models.CharField(blank=True, max_length=256)
    year = models.IntegerField(blank=True)
    description = models.TextField()
    category = models.ForeignKey(
        'Categories', on_delete=models.SET_DEFAULT, related_name='titles',
        blank=True, default='not_chosen')

    def average_rating(self) -> int:
        # Первый способ как из статьи с сайта, тут нужна модель
        # Reviews

        # rating = Reviews.objects.filter(title=self).aggregate(
        #     avg_rating=models.Avg('score'))['avg_rating'] or 0

        # Второй способ нашла в документации через "annotate"
        # "reviews" - это related_name модели Reviews поля title
        rating = Titles.objects.filter(name=self).annotate(
            avg_rating=models.Avg('reviews'))['avg_rating'] or 0
        return int(rating)

    def __str__(self) -> str:
        return self.name
