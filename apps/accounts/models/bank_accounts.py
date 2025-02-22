from decimal import Decimal

from django.db import models

from apps.core.models.base import BaseModel
from apps.core.models.currency import Currencies
from .chart_of_accounts import ChartOfAccount
from .banks import Bank


class BankAccount(BaseModel):
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT)  # Foreign Key to Bank
    account_number = models.CharField(max_length=50)
    iban = models.CharField(max_length=50, null=True, blank=True)
    swift_code = models.CharField(max_length=20, null=True, blank=True)
    account = models.OneToOneField(
        ChartOfAccount,
        on_delete=models.PROTECT
    )
    branch_name = models.CharField(max_length=255, null=True, blank=True)
    currency = models.IntegerField(choices=Currencies.choices, default=Currencies.USD)
    account_type = models.CharField(max_length=50, choices=[('checking', 'Checking'), ('savings', 'Savings')], default='checking')  # Added account type
    opening_balance = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00')) # Changed to DecimalField
    current_balance = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00')) # Changed to DecimalField

    def __str__(self):
        return f"{self.bank.name} - {self.account_number}"

    class Meta:
        unique_together = [['org', 'account_number'], ['org', 'iban']]

