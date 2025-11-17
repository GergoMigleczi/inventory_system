from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import Category, UnitOfMeasure, Product
from .forms import CategoryForm, UnitsOfMeasureForm, ProductForm
from django.db.models.deletion import ProtectedError
from django.contrib import messages
from django.shortcuts import redirect
from inventory_system.utils.urlbuilder import UrlBuilder



class CategoryListView(ListView):
    model = Category
    template_name = "list_base.html"
    context_object_name = "rows"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "title": "Categories",
            "columns": ["name", "parent"],
            "new_builder": UrlBuilder("category_create", []),
            "edit_builder": UrlBuilder("category_edit", ["pk"]),
            "delete_builder": UrlBuilder("category_delete", ["pk"]),
        })

        return context

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "form_base.html"
    success_url = reverse_lazy("category_list")

    extra_context = {
        "title": "Add Category",
        "cancel_url": reverse_lazy("category_list"),
    }

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "form_base.html"
    success_url = reverse_lazy("category_list")

    extra_context = {
        "title": "Edit Category",
        "cancel_url": reverse_lazy("category_list"),
    }

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("category_list")

    extra_context = {
        "title": "Delete Category",
        "cancel_url": reverse_lazy("category_list"),
    }

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                "Cannot delete this category because products are linked to it."
            )
            return redirect(self.success_url)

class UnitListView(ListView):
    model = UnitOfMeasure
    template_name = "list_base.html"
    context_object_name = "rows"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "title": "Units of Measure",
            "columns": ["short_code", "name"],
            "new_builder": UrlBuilder("unit_create", []),
            "edit_builder": UrlBuilder("unit_edit", ["pk"]),
            "delete_builder": UrlBuilder("unit_delete", ["pk"]),
        })

        return context

class UnitCreateView(CreateView):
    model = UnitOfMeasure
    form_class = UnitsOfMeasureForm
    template_name = "form_base.html"
    success_url = reverse_lazy("unit_list")

    extra_context = {
        "title": "Add Unit of Measure",
        "cancel_url": reverse_lazy("unit_list"),
    }

class UnitUpdateView(UpdateView):
    model = UnitOfMeasure
    form_class = UnitsOfMeasureForm
    template_name = "form_base.html"
    success_url = reverse_lazy("unit_list")

    extra_context = {
        "title": "Edit Unit of Measure",
        "cancel_url": reverse_lazy("unit_list"),
    }

class UnitDeleteView(DeleteView):
    model = UnitOfMeasure
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("unit_list")

    extra_context = {
        "title": "Delete Unit of Measure",
        "cancel_url": reverse_lazy("unit_list"),
    }

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                "Cannot delete this unit because products are linked to it."
            )
            return redirect(self.success_url)
        
class ProductListView(ListView):
    model = Product
    template_name = "list_base.html"
    context_object_name = "rows"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "title": "Products",
            "columns": ["name", "category", "unit"],
            "new_builder": UrlBuilder("product_create", []),
            "edit_builder": UrlBuilder("product_edit", ["pk"]),
            "delete_builder": UrlBuilder("product_delete", ["pk"]),
        })

        return context

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "form_base.html"
    success_url = reverse_lazy("product_list")

    extra_context = {
        "title": "Add Product",
        "cancel_url": reverse_lazy("product_list"),
    }

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "form_base.html"
    success_url = reverse_lazy("product_list")

    extra_context = {
        "title": "Edit Product",
        "cancel_url": reverse_lazy("product_list"),
    }

class ProductDeleteView(DeleteView):
    model = Product
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("Product_list")

    extra_context = {
        "title": "Delete Product",
        "cancel_url": reverse_lazy("product_list"),
    }