from django.db import models

from apps.core.models import BaseModel


class Warehouse(BaseModel):
    name = models.CharField(max_length=100)
    address = models.TextField()
    is_default = models.BooleanField(default=False)

    class Meta:
        unique_together = [['org', 'code']]