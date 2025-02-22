from django.db import models
from apps.core.models.base import BaseModel


class Bank(BaseModel):
    name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    swift_code = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name

