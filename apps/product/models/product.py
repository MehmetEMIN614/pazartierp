from decimal import Decimal

from django.db import models

from apps.accounts.models import ChartOfAccount
from apps.core.models import BaseModel
from apps.product.models import ProductCategory
from apps.product.models.uom import UnitOfMeasure


class Product(BaseModel):
    name = models.CharField(max_length=255)  # Ürün adı
    code = models.CharField(max_length=50, unique=True)  # Ürün kodu (benzersiz)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name='products')  # Ürün kategorisi
    description = models.TextField(blank=True, null=True)  # Ürün açıklaması
    list_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # Liste fiyatı
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # Maliyet fiyatı
    standard_price = models.DecimalField(max_digits=10, decimal_places=2,
                                         default=Decimal('0.00'))  # Standart fiyat (maliyet hesabı için)
    track_inventory = models.BooleanField(default=True)  # Stok takibi yapılıp yapılmaması
    uom = models.ForeignKey(UnitOfMeasure, on_delete=models.PROTECT)  # Ölçü birimi
    min_quantity = models.DecimalField(max_digits=10, decimal_places=2,
                                       default=Decimal('0.00'))  # Minimum stok seviyesi
    max_quantity = models.DecimalField(max_digits=10, decimal_places=2,
                                       default=Decimal('0.00'))  # Maksimum stok seviyesi
    income_account = models.ForeignKey(ChartOfAccount, on_delete=models.PROTECT,
                                       related_name='income_products')  # Gelir hesabı
    expense_account = models.ForeignKey(ChartOfAccount, on_delete=models.PROTECT,
                                        related_name='expense_products')  # Gider (maliyet) hesabı

    # ... diğer alanlar (örneğin, resim, özellikler, vergi bilgisi vb.) ...

    class Meta:
        unique_together = [['org', 'code']]

    def __str__(self):
        return self.name
