from django.urls import path
from .views import (
    WarehouseListView,
    WarehouseCreateView,
    WarehouseUpdateView,
    WarehouseDeleteView,
    ProductBatchListView,
    ProductBatchCreateView,
    ProductBatchUpdateView,
    ProductBatchDeleteView,
)

urlpatterns = [
    # Warehouses
    path('', WarehouseListView.as_view(), name="warehouse_list"),
    path('new/', WarehouseCreateView.as_view(), name="warehouse_create"),
    path('<int:warehouse_id>/edit/', WarehouseUpdateView.as_view(), name="warehouse_edit"),
    path('<int:warehouse_id>/delete/', WarehouseDeleteView.as_view(), name="warehouse_delete"),

    # Product Batches (per warehouse)
    path('<int:warehouse_id>/batches/', ProductBatchListView.as_view(), name="warehouse_batches"),
    path('<int:warehouse_id>/batches/new/', ProductBatchCreateView.as_view(), name="warehouse_batch_create"),
    path('<int:warehouse_id>/batches/<int:batch_id>/edit/', ProductBatchUpdateView.as_view(), name="warehouse_batch_edit"),
    path('<int:warehouse_id>/batches/<int:batch_id>/delete/', ProductBatchDeleteView.as_view(), name="warehouse_batch_delete"),
]
