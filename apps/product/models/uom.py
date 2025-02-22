from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import BaseModel


class UnitOfMeasure(BaseModel):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)
    category = models.CharField(
        max_length=20,
        choices=[
            ('UNIT', _('Unit')),
            ('WEIGHT', _('Weight')),
            ('LENGTH', _('Length')),
            ('VOLUME', _('Volume')),
            ('TIME', _('Time'))
        ]
    )
    ratio = models.FloatField(default=0)

    class Meta:
        unique_together = [['org', 'name']]
