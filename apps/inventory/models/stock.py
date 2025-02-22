from django.db import models
from apps.core.models import BaseModel
from decimal import Decimal

from apps.inventory.models.stock_location import StockLocation
from apps.product.models.product import Product


class Stock(BaseModel):
    location = models.ForeignKey(StockLocation, on_delete=models.CASCADE, related_name='stock_items') # Stok konumu
    product = models.ForeignKey(Product, on_delete=models.CASCADE) # Ürün
    quantity = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00')) # Mevcut miktar
    # ... diğer alanlar (örneğin, seri numaraları, son kullanım tarihi vb.) ...

    class Meta:
        unique_together = [['location', 'product']]

    def __str__(self):
        return f"{self.location} - {self.product} ({self.quantity})"
