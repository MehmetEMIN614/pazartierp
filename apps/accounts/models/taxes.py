from django.db import models
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

from apps.core.models.base import BaseModel
from .chart_of_accounts import ChartOfAccount


class TaxType(models.TextChoices):
    PERCENTAGE = 'percentage', _('Percentage')
    FIXED = 'fixed', _('Fixed Amount')


class Tax(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=TaxType.choices)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Store tax rate explicitly
    tax_type = models.CharField(max_length=50, choices=[('vat', 'VAT'), ('sales_tax', 'Sales Tax')], default='vat')  # More specific tax type
    account = models.ForeignKey(
        ChartOfAccount,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    include_base_amount = models.BooleanField(default=False)

    def __str__(self):
        return self.name

