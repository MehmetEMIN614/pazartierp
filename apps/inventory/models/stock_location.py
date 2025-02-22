from django.db import models

from apps.core.models import BaseModel
from apps.inventory.models.warehouse import Warehouse


class StockLocation(BaseModel):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='locations')  # Depo
    name = models.CharField(max_length=255)  # Stok konumu adı (örneğin, "Raf A", "Bölüm 1")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='children')  # Üst konum (hiyerarşik yapı için)

    # ... diğer alanlar ...

    class Meta:
        unique_together = [['warehouse', 'name']]

    def __str__(self):
        return f"{self.warehouse.name} - {self.name}"
