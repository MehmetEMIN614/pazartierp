from django.db import models
from apps.core.models import BaseModel
from apps.contact.models import Contact
from apps.product.models import Product


class SalesOrder(BaseModel):
    STATE_CHOICES = (
        ('draft', 'Taslak'),
        ('sent', 'Gönderildi'),
        ('approved', 'Onaylandı'),
        ('shipped', 'Sevk Edildi'),
        ('invoiced', 'Fatura Kesildi'),
        ('cancelled', 'İptal Edildi'),
    )

    contact = models.ForeignKey(Contact, on_delete=models.PROTECT, related_name='sales_orders')
    reference = models.CharField(max_length=50, blank=True, null=True) # Referans numarası
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='draft')
    expected_date = models.DateField(blank=True, null=True) # Beklenen teslim tarihi
    note = models.TextField(blank=True, null=True) # Notlar

    def __str__(self):
        return f"Satış Siparişi #{self.id} - {self.contact.display_name}"

