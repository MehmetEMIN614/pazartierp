from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import BaseModel


class AccountType(models.TextChoices):
    ASSET = 'ASSET', _('Asset')
    LIABILITY = 'LIABILITY', _('Liability')
    EQUITY = 'EQUITY', _('Equity')
    REVENUE = 'REVENUE', _('Revenue')
    EXPENSE = 'EXPENSE', _('Expense')


class ChartOfAccount(BaseModel):
    code_prefix = models.CharField(max_length=10)  # Added prefix
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=20, choices=AccountType.choices)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )
    is_reconcilable = models.BooleanField(default=False)
    allow_reconciliation = models.BooleanField(default=False)
    reconcile_date = models.DateField(null=True, blank=True)  # Added reconcile date
    balance_type = models.CharField(max_length=10, choices=[('balance_sheet', 'Balance Sheet'), ('income_statement', 'Income Statement')], default='balance_sheet')  # Added balance type
    current_balance = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))  # Changed to DecimalField

    def __str__(self):
        return f"{self.code_prefix}{self.code} - {self.name}"  # Modified __str__

    class Meta:
        verbose_name = _('Chart of Account')
        verbose_name_plural = _('Chart of Accounts')
        unique_together = [['org', 'code']]

