from django.db import models
from apps.core.models.base import BaseModel
from .account_move_lines import AccountMoveLine


class AccountReconciliation(BaseModel):
    bank_account = models.ForeignKey('accounts.BankAccount', on_delete=models.PROTECT)
    statement_date = models.DateField()
    reconciled_lines = models.ManyToManyField(AccountMoveLine, blank=True)
    # Add fields for statement details (e.g., file upload) as needed

    def __str__(self):
        return f"Reconciliation for {self.bank_account} on {self.statement_date}"

