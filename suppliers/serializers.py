from rest_framework import serializers
from .models import Supplier, SupplierProduct
from products.models import Product


class SupplierProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = SupplierProduct
        fields = [
            "id",
            "product_id",
            "product_name",
            "supplier_sku",
            "cost_price",
            "lead_time_days",
            "is_primary",
        ]


class SupplierSerializer(serializers.ModelSerializer):
    products = SupplierProductSerializer(many=True, source="supplierproduct_set", read_only=True)

    class Meta:
        model = Supplier
        fields = [
            "id",
            "name",
            "contact_name",
            "email",
            "phone",
            "address_line1",
            "address_line2",
            "city",
            "postcode",
            "country",
            "is_active",
            "created_at",
            "products",
        ]
