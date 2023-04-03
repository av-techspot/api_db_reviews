from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def actual_year(value) -> None:
    if value > datetime.now().year or value <= 0:
        raise ValidationError(
            _('%(value)s некорректное значение года'), params={'value': value},
        )
