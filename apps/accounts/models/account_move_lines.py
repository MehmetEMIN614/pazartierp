from decimal import Decimal

from django.db import models

from apps.core.models.base import BaseModel
from apps.core.models.currency import Currencies
from .account_moves import AccountMove
from .chart_of_accounts import ChartOfAccount
from .taxes import Tax  # Import Tax Model
from ...contact.models import Contact


class AccountMoveLine(BaseModel):
    move = models.ForeignKey(
        AccountMove,
        on_delete=models.CASCADE,
        related_name='lines'
    )
    account = models.ForeignKey(
        ChartOfAccount,
        on_delete=models.PROTECT
    )
    debit = models.DecimalField(max_digits=20, decimal_places=2,
                                default=Decimal('0.00'))  # changed to debit and DecimalField
    credit = models.DecimalField(max_digits=20, decimal_places=2,
                                 default=Decimal('0.00'))  # changed to credit and DecimalField
    currency = models.IntegerField(choices=Currencies.choices, default=Currencies.USD)
    amount_currency = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,  # Assuming you want to allow null contacts.  Adjust as needed.
        null=True,
        blank=True
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    reconciled = models.BooleanField(default=False)
    tax_ids = models.ManyToManyField(Tax, blank=True)  # Added ManyToManyField for taxes
    analytic_account_id = models.ForeignKey('accounts.AnalyticAccount', on_delete=models.SET_NULL, null=True,
                                            blank=True)  # Added Analytic Account

    def __str__(self):
        return f"{self.account.name} - Debit: {self.debit}, Credit: {self.credit}"  # Modified __str__

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(debit__gte=0, credit=0) | models.Q(debit=0, credit__gte=0),
                                   name='debit_or_credit_positive')
        ]
