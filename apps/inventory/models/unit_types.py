from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import BaseModel


class UnitType(BaseModel):
    name = models.CharField(max_length=50, unique=True)  # Ölçü birimi tipi adı (örneğin, "Ağırlık", "Hacim", "Uzunluk")
    description = models.TextField(blank=True, null=True)  # Açıklama

    class Meta:
        verbose_name = _("Unit Type")
        verbose_name_plural = _("Unit Types")
        unique_together = [['org', 'name']]

    def __str__(self):
        return self.name
