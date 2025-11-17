from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children"
    )

    def __str__(self):
        return self.name


class UnitOfMeasure(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.short_code or self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, null=True, blank=True
    )
    unit = models.ForeignKey(
        UnitOfMeasure, on_delete=models.PROTECT
    )

    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.unit.short_code})"
