from django.urls import path
from .views import (
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    UnitListView, UnitCreateView, UnitUpdateView, UnitDeleteView,
    ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView
)

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("categories/new/", CategoryCreateView.as_view(), name="category_create"),
    path("categories/<int:pk>/edit/", CategoryUpdateView.as_view(), name="category_edit"),
    path("categories/<int:pk>/delete/", CategoryDeleteView.as_view(), name="category_delete"),

    path("units/", UnitListView.as_view(), name="unit_list"),
    path("units/new/", UnitCreateView.as_view(), name="unit_create"),
    path("units/<int:pk>/edit/", UnitUpdateView.as_view(), name="unit_edit"),
    path("units/<int:pk>/delete/", UnitDeleteView.as_view(), name="unit_delete"),

    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/new/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_edit"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
]
