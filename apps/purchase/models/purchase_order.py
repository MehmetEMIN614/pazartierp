from django.db import models

from apps.core.models import BaseModel


class PurchaseOrder(BaseModel):
    STATE_CHOICES = (
        ('taslak', 'Taslak'),
        ('gönderildi', 'Gönderildi'),
        ('onaylandı', 'Onaylandı'),
        ('kısmen_teslim_alındı', 'Kısmen Teslim Alındı'),
        ('teslim_alındı', 'Teslim Alındı'),
        ('fatura_kesildi', 'Fatura Kesildi'),
        ('ödendi', 'Ödendi'),
        ('iptal_edildi', 'İptal Edildi'),
    )
    reference = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='taslak')
    note = models.TextField(blank=True, null=True)
    total_amount_currency = models.DecimalField(max_digits=15, decimal_places=2,
                                                default=0)  # Total amount in order currency
    total_amount_usd = models.DecimalField(max_digits=15, decimal_places=2, null=True,
                                           blank=True)  # Total amount in USD

    def __str__(self):
        return f"Satın Alma Siparişi #{self.id}"

    def save(self, *args, **kwargs):
        self.calculate_totals()
        super().save(*args, **kwargs)

    def calculate_totals(self):
        total_amount_currency = sum(line.amount_currency for line in self.lines.all())
        self.total_amount_currency = total_amount_currency
        total_amount_usd = sum(line.amount_usd for line in self.lines.all())
        self.total_amount_usd = total_amount_usd
