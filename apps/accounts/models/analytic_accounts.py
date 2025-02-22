from django.db import models
from apps.core.models.base import BaseModel


class AnalyticAccount(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

