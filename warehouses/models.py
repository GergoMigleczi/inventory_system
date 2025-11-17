from django.db import models
from products.models import Product

class Warehouse(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255, blank=True)

    class Meta:
            unique_together = ("name", "location")

    def __str__(self):
        return f"{self.name} ({self.location})"


class ProductBatch(models.Model):
    goods_receipt_line = models.OneToOneField(
        "purchasing.GoodsReceiptLine",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="batch",
        )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField()
    lot_number = models.CharField(max_length=100, blank=True)

