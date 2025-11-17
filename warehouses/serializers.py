from rest_framework import serializers
from .models import Warehouse, ProductBatch, Product, Warehouse


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'location']


class ProductBatchSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)

    class Meta:
        model = ProductBatch
        fields = [
            'id',
            'product_id',
            'product_name',
            'warehouse_name',
            'quantity',
            'expiry_date',
            'lot_number'
        ]
    