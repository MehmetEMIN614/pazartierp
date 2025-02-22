from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import BaseModel
from .chart_of_accounts import ChartOfAccount


class Journal(BaseModel):
    name = models.CharField(max_length=255)
    code_prefix = models.CharField(max_length=10)  # Added prefix
    code = models.CharField(max_length=10, unique=True)
    type = models.CharField(
        max_length=50,
        choices=[
            ('SALE', _('Sales')),
            ('PURCHASE', _('Purchases')),
            ('CASH', _('Cash')),
            ('BANK', _('Bank')),
            ('GENERAL', _('General'))
        ]
    )
    sequence_code = models.CharField(max_length=20)
    default_credit_account = models.ForeignKey(
        ChartOfAccount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='credit_journals'
    )
    default_debit_account = models.ForeignKey(
        ChartOfAccount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='debit_journals'
    )
    is_posted = models.BooleanField(default=False)  # Added is_posted field

    def __str__(self):
        return f"{self.code_prefix}{self.code} - {self.name}"  # Modified __str__

    class Meta:
        unique_together = [['org', 'code'], ['org', 'sequence_code']]

