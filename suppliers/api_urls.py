from django.urls import path
from .views_api import (
    suppliers_root,
    SupplierListCreateView,
    SupplierDetailView,
    SupplierProductListCreateView,
)

urlpatterns = [
    path("", suppliers_root),
    path("list/", SupplierListCreateView.as_view(), name="api_supplier_list"),
    path("<int:pk>/", SupplierDetailView.as_view(), name="api_supplier_detail"),
    path("<int:supplier_id>/products/", SupplierProductListCreateView.as_view(),
         name="api_supplier_products"),
]
