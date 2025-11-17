from django.urls import path
from .views import (
    SupplierListView,
    SupplierCreateView,
    SupplierUpdateView,
    SupplierDeleteView,
    SupplierProductListView,
    SupplierProductCreateView,
    SupplierProductUpdateView,
    SupplierProductDeleteView,
)

urlpatterns = [
    path("", SupplierListView.as_view(), name="supplier_list"),
    path("new/", SupplierCreateView.as_view(), name="supplier_create"),
    path("<int:supplier_id>/edit/", SupplierUpdateView.as_view(), name="supplier_edit"),
    path("<int:supplier_id>/delete/", SupplierDeleteView.as_view(), name="supplier_delete"),
    path("<int:supplier_id>/products/", SupplierProductListView.as_view(), name="supplier_products"),
    path("<int:supplier_id>/products/new/", SupplierProductCreateView.as_view(), name="supplier_product_create"),
    path("<int:supplier_id>/products/<int:supplier_product_id>/edit/", SupplierProductUpdateView.as_view(), name="supplier_product_edit"),
    path("<int:supplier_id>/products/<int:supplier_product_id>/delete/", SupplierProductDeleteView.as_view(), name="supplier_product_delete"),
]
