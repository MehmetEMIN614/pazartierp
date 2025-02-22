from decimal import Decimal

from django.db import models

from apps.core.models import BaseModel
from apps.inventory.models.unit_types import UnitType
from apps.product.models.product import Product
from apps.product.models.uom import UnitOfMeasure


class ProductUnit(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='units')  # Ürün
    unit = models.ForeignKey(UnitOfMeasure, on_delete=models.PROTECT)  # Ölçü birimi
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # Fiyat
    quantity = models.DecimalField(max_digits=10, decimal_places=3, default=Decimal('1.000'))  # Miktar (bu birim için)
    unit_type = models.ForeignKey(UnitType, on_delete=models.PROTECT)  # UnitType modelini referans alır

    class Meta:
        unique_together = [['product', 'unit']]

    def __str__(self):
        return f"{self.product.name} - {self.unit.name} ({self.price})"
