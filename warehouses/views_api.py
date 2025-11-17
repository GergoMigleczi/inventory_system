from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Warehouse, ProductBatch
from .serializers import WarehouseSerializer, ProductBatchSerializer


@api_view(["GET"])
def warehouse_root(request):
    return Response({
        "list_warehouses": "/api/warehouse/list/",
        "warehouse_detail": "/api/warehouse/<id>/",
        "warehouse_batches": "/api/warehouse/<id>/batches/",
    })


class WarehouseListCreateView(generics.ListCreateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]


class WarehouseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]


class ProductBatchListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductBatchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProductBatch.objects.filter(warehouse_id=self.kwargs["warehouse_id"])

    def perform_create(self, serializer):
        warehouse = Warehouse.objects.get(id=self.kwargs["warehouse_id"])
        serializer.save(warehouse=warehouse)

