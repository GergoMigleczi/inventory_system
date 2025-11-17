from rest_framework import viewsets
from .models import Product, Category, UnitOfMeasure
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    UnitSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UnitViewSet(viewsets.ModelViewSet):
    queryset = UnitOfMeasure.objects.all()
    serializer_class = UnitSerializer
