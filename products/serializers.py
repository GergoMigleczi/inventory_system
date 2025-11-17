from rest_framework import serializers
from .models import Category, UnitOfMeasure, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "parent"]


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasure
        fields = ["id", "name", "short_code"]


class ProductSerializer(serializers.ModelSerializer):
    # Read-only nested objects
    category = CategorySerializer(read_only=True)
    unit = UnitSerializer(read_only=True)

    # Write-only strings for input
    category_name = serializers.CharField(write_only=True)
    unit_short_code = serializers.CharField(write_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "sku",
            "description",
            "category",
            "unit",
            "category_name",
            "unit_short_code",
            "active",
        ]
    
    def create(self, validated_data):
        category_name = validated_data.pop("category_name")
        unit_short_code = validated_data.pop("unit_short_code")

        # Resolve category
        category = Category.objects.get(name=category_name)

        # Resolve unit of measure
        unit = UnitOfMeasure.objects.get(short_code=unit_short_code)

        product = Product.objects.create(
            category=category,
            unit=unit,
            **validated_data
        )
        return product

    def update(self, instance, validated_data):
        category_name = validated_data.pop("category_name", None)
        unit_short_code = validated_data.pop("unit_short_code", None)

        if category_name:
            instance.category = Category.objects.get(name=category_name)

        if unit_short_code:
            instance.unit = UnitOfMeasure.objects.get(short_code=unit_short_code)

        return super().update(instance, validated_data)
