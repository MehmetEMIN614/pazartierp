from django.db import models
from apps.core.models.base import BaseModel, BaseModelNoOrg


class Org(BaseModelNoOrg):
    name = models.CharField(max_length=128, unique=True)
    address = models.TextField(max_length=1024, null=True, blank=True)
    note = models.TextField(max_length=512, null=True, blank=True)

    class Meta:
        verbose_name = 'Org'
        verbose_name_plural = 'Orgs'

    def __str__(self):
        return self.name


class OrgSetting(BaseModel):
    org = models.OneToOneField(
        Org,
        on_delete=models.CASCADE,
        related_name='settings'
    )
    language = models.CharField(max_length=10, default='en-us')
    timezone = models.CharField(max_length=50, default='UTC')
    decimal_precision = models.IntegerField(default=2)
