from django.urls import path
from .views_api import (
    warehouse_root,
    WarehouseListCreateView,
    WarehouseDetailView,
    ProductBatchListCreateView,
)

urlpatterns = [
    path("", warehouse_root),
    path("list/", WarehouseListCreateView.as_view(), name="api_warehouse_list"),
    path("<int:pk>/", WarehouseDetailView.as_view(), name="api_warehouse_detail"),
    path("<int:warehouse_id>/batches/", ProductBatchListCreateView.as_view(),
         name="api_warehouse_batches"),
]
