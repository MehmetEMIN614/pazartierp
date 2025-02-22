from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import BaseModel


class ProductCategory(BaseModel):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )
    note = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Product Categories'
        unique_together = [['org', 'name']]

    def __str__(self):
        return self.name


