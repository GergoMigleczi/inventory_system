from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Supplier, SupplierProduct
from .serializers import SupplierSerializer, SupplierProductSerializer


@api_view(["GET"])
def suppliers_root(request):
    return Response({
        "list_suppliers": "/api/suppliers/list/",
        "supplier_detail": "/api/suppliers/<id>/",
        "supplier_products": "/api/suppliers/<id>/products/",
    })


class SupplierListCreateView(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]


class SupplierDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]


class SupplierProductListCreateView(generics.ListCreateAPIView):
    serializer_class = SupplierProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SupplierProduct.objects.filter(supplier_id=self.kwargs["supplier_id"])

    def perform_create(self, serializer):
        serializer.save(supplier_id=self.kwargs["supplier_id"])
