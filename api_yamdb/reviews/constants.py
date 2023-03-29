from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class UserRoles(TextChoices):
    USER = 'user', _('Потльзователь')
    MODERATOR = 'moderator', _('Модератор')
    ADMIN = 'admin', _('Администратор')
