from django.db import models

from apps.accounts.models import ChartOfAccount, Tax
from apps.core.models import BaseModel, Currencies, CurrencyRate
from apps.product.models import Product
from apps.sales.models.sales_order import SalesOrder


class SalesOrderLine(BaseModel):
    order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='lines')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    currency = models.IntegerField(choices=Currencies.choices, default=Currencies.USD)  # Para birimi
    quantity = models.DecimalField(max_digits=12, decimal_places=2)  # Miktar
    unit_price_currency = models.DecimalField(max_digits=10, decimal_places=2)  # Birim fiyatı
    unit_price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    amount_currency = models.DecimalField(max_digits=15, decimal_places=2)  # Tutar (işlem para biriminde)
    amount_usd = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)  # USD karşılığı tutar
    usd_rate = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)  # Özel kur oranı

    tax_ids = models.ManyToManyField(Tax, blank=True)  # Vergi bilgisi

    # Accounting related
    account = models.ForeignKey(ChartOfAccount, on_delete=models.PROTECT, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.calculate_amounts()
        super().save(*args, **kwargs)

    def calculate_amounts(self):
        self.amount_currency = self.unit_price_currency * self.quantity
        if self.usd_rate:
            self.unit_price_usd = self.unit_price_currency * self.usd_rate
            self.amount_usd = self.amount_currency * self.usd_rate
        else:
            try:
                rate = CurrencyRate.get_rate(self.currency, Currencies.USD)
                self.unit_price_usd = self.unit_price_currency * rate
                self.amount_usd = self.amount_currency * rate
            except ValueError:
                self.unit_price_usd = None
                self.amount_usd = None
