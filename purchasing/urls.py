from django.urls import path
from .views import (
    PurchaseOrderListView,
    PurchaseOrderCreateView,
    PurchaseOrderUpdateView,
    PurchaseOrderDeleteView,
    PurchaseOrderLineListView,
    PurchaseOrderLineCreateView,
    PurchaseOrderLineUpdateView,
    PurchaseOrderLineDeleteView,

    GoodsReceiptListView,
    GoodsReceiptCreateView,
    GoodsReceiptUpdateView,
    GoodsReceiptDeleteView,
    GoodsReceiptLineListView,
    GoodsReceiptLineCreateView,
    GoodsReceiptLineUpdateView,
    GoodsReceiptLineDeleteView,
    
)

urlpatterns = [
    path("purchase_orders", PurchaseOrderListView.as_view(), name="purchase_order_list"),
    path("purchase_orders/new/", PurchaseOrderCreateView.as_view(), name="purchase_order_create"),
    path("purchase_orders/<int:purchase_order_id>/edit/", PurchaseOrderUpdateView.as_view(), name="purchase_order_edit"),
    path("purchase_orders/<int:purchase_order_id>/delete/", PurchaseOrderDeleteView.as_view(), name="purchase_order_delete"),
    path("purchase_orders/<int:purchase_order_id>/line_items/", PurchaseOrderLineListView.as_view(), name="purchase_order_line_items"),
    path("purchase_orders/<int:purchase_order_id>/line_items/new/", PurchaseOrderLineCreateView.as_view(), name="purchase_order_line_create"),
    path("purchase_orders/<int:purchase_order_id>/line_items/<int:purchase_order_line_id>/edit/", PurchaseOrderLineUpdateView.as_view(), name="purchase_order_line_edit"),
    path("purchase_orders/<int:purchase_order_id>/line_items/<int:purchase_order_line_id>/delete/", PurchaseOrderLineDeleteView.as_view(), name="purchase_order_line_delete"),

    path("goods_receipts", GoodsReceiptListView.as_view(), name="goods_receipt_list"),
    path("goods_receipts/new/", GoodsReceiptCreateView.as_view(), name="goods_receipt_create"),
    path("goods_receipts/<int:goods_receipt_id>/edit/", GoodsReceiptUpdateView.as_view(), name="goods_receipt_edit"),
    path("goods_receipts/<int:goods_receipt_id>/delete/", GoodsReceiptDeleteView.as_view(), name="goods_receipt_delete"),
    path("goods_receipts/<int:goods_receipt_id>/line_items/", GoodsReceiptLineListView.as_view(), name="goods_receipt_line_items"),
    path("goods_receipts/<int:goods_receipt_id>/line_items/new/", GoodsReceiptLineCreateView.as_view(), name="goods_receipt_line_create"),
    path("goods_receipts/<int:goods_receipt_id>/line_items/<int:goods_receipt_line_id>/edit/", GoodsReceiptLineUpdateView.as_view(), name="goods_receipt_line_edit"),
    path("goods_receipts/<int:goods_receipt_id>/line_items/<int:goods_receipt_line_id>/delete/", GoodsReceiptLineDeleteView.as_view(), name="goods_receipt_line_delete"),


]
