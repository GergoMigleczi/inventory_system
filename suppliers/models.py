from django.db import models
from products.models import Product


class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True)
    contact_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)

    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SupplierProduct(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    supplier_sku = models.CharField(max_length=255, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    lead_time_days = models.PositiveIntegerField(default=0)

    is_primary = models.BooleanField(default=False)

    class Meta:
        unique_together = ("supplier", "product")

    def __str__(self):
        return f"{self.supplier.name} → {self.product.name}"
