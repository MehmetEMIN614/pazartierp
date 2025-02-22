from django.db import models

from apps.accounts.models import ChartOfAccount, Tax
from apps.contact.models import Contact
from apps.core.models import BaseModel, Currencies, CurrencyRate
from apps.product.models import Product
from apps.purchase.models import PurchaseOrder


class PurchaseOrderLine(BaseModel):
    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='lines')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT)  # Tedarikçi
    quantity = models.DecimalField(max_digits=12, decimal_places=2)  # Miktar
    unit_price_currency = models.DecimalField(max_digits=10, decimal_places=2)  # Birim fiyat (işlem para biriminde)
    currency = models.IntegerField(choices=Currencies.choices, default=Currencies.TRY)  # Para birimi
    amount_currency = models.DecimalField(max_digits=15, decimal_places=2)  # Tutar (işlem para biriminde)
    unit_price_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True,
                                         blank=True)  # USD karşılığı birim fiyat
    amount_usd = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)  # USD karşılığı tutar
    custom_rate = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)  # Özel kur oranı
    tax_ids = models.ManyToManyField(Tax, blank=True)  # Vergi bilgisi

    # Muhasebe ile ilgili alanlar
    account = models.ForeignKey(ChartOfAccount, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} adet ({self.contact.display_name})"

    def save(self, *args, **kwargs):
        self.calculate_amounts()
        super().save(*args, **kwargs)

    def calculate_amounts(self):
        self.amount_currency = self.unit_price_currency * self.quantity
        if self.custom_rate:
            self.unit_price_usd = self.unit_price_currency * self.custom_rate
            self.amount_usd = self.amount_currency * self.custom_rate
        else:
            try:
                rate = CurrencyRate.get_rate(self.currency, Currencies.USD)
                self.unit_price_usd = self.unit_price_currency * rate
                self.amount_usd = self.amount_currency * rate
            except ValueError:
                self.unit_price_usd = None
                self.amount_usd = None
