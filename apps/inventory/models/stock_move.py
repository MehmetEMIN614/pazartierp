from django.db import models

from apps.core.models import BaseModel
from apps.inventory.models.stock_location import StockLocation
from apps.product.models.product import Product


class StockMove(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)  # Ürün
    from_location = models.ForeignKey(StockLocation, on_delete=models.PROTECT,
                                      related_name='stock_moves_from')  # Kaynak konum
    to_location = models.ForeignKey(StockLocation, on_delete=models.PROTECT,
                                    related_name='stock_moves_to')  # Hedef konum
    quantity = models.DecimalField(max_digits=12, decimal_places=2)  # Miktar
    state = models.CharField(max_length=20,
                             choices=[('draft', 'Taslak'), ('pending', 'Beklemede'), ('done', 'Tamamlandı'),
                                      ('cancelled', 'İptal Edildi')], default='draft')  # Hareket durumu
    reference = models.CharField(max_length=100, blank=True, null=True)  # Referans numarası
    scheduled_date = models.DateTimeField()  # Planlanan tarih
    effective_date = models.DateTimeField(blank=True, null=True)  # Gerçekleşen tarih

    def __str__(self):
        return f"{self.product.name} - {self.from_location} -> {self.to_location} ({self.quantity})"
