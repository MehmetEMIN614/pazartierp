from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import BaseModel
from .journals import Journal


class AccountMove(BaseModel):
    MOVE_STATE_CHOICES = [
        ('DRAFT', _('Draft')),
        ('OPEN', _('Open')),  # Added Open state
        ('POSTED', _('Posted')),
        ('CANCELLED', _('Cancelled'))
    ]

    date = models.DateField()
    journal = models.ForeignKey(
        Journal,
        on_delete=models.PROTECT,
        related_name='moves'
    )
    name = models.CharField(max_length=255, blank=True, null=True)  # Added name
    reference = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=20, choices=MOVE_STATE_CHOICES, default='DRAFT')
    narration = models.TextField(null=True, blank=True)
    date_posted = models.DateTimeField(null=True, blank=True)  # Added date_posted
    total_debit = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))  # Changed to DecimalField
    total_credit = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))  # Changed to DecimalField

    def __str__(self):
        return f"{self.journal.name} - {self.date}"

    def calculate_totals(self):
        debit_lines = self.lines.filter(debit__gt=0)
        credit_lines = self.lines.filter(credit__gt=0)
        self.total_debit = sum(line.debit for line in debit_lines)
        self.total_credit = sum(line.credit for line in credit_lines)
        return self.total_debit == self.total_credit

