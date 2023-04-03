from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

CHAR_LIMITS_REVIEW = 20


class UserRoles(TextChoices):
    USER = 'user', _('Пользователь')
    MODERATOR = 'moderator', _('Модератор')
    ADMIN = 'admin', _('Администратор')
