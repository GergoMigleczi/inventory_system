from django.urls import reverse_lazy
from django.db import IntegrityError
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from .forms import SupplierForm, SupplierProductForm
from .models import Supplier, SupplierProduct
from inventory_system.utils.urlbuilder import UrlBuilder
from inventory_system.utils.recordheader import RecordHeader


from .models import Supplier


class SupplierListView(ListView):
    model = Supplier
    template_name = "list_base.html"
    context_object_name = "rows"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "title": "Suppliers",
            "columns": ["name", "email", "phone"],
            "new_builder": UrlBuilder("supplier_create", []),
            "edit_builder": UrlBuilder("supplier_edit", ["pk"]),
            "delete_builder": UrlBuilder("supplier_delete", ["pk"]),
            "extra_actions": [
                {
                    "label": "Products",
                    # /suppliers/<id>/products/
                    "builder": UrlBuilder("supplier_products", ["pk"]),
                }
            ],
        })

        return context


class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = "form_base.html"
    success_url = reverse_lazy("supplier_list")

    extra_context = {
        "title": "Add Supplier",
        "cancel_url": reverse_lazy("supplier_list"),
    }


class SupplierUpdateView(UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = "form_base.html"

    pk_url_kwarg = "supplier_id"
    success_url = reverse_lazy("supplier_list")

    extra_context = {
        "title": "Edit Supplier",
        "cancel_url": reverse_lazy("supplier_list"),
    }


class SupplierDeleteView(DeleteView):
    model = Supplier
    template_name = "confirm_delete.html"

    pk_url_kwarg = "supplier_id"
    success_url = reverse_lazy("supplier_list")

    extra_context = {
        "title": "Delete Supplier",
        "cancel_url": reverse_lazy("supplier_list"),
    }

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Exception:
            messages.error(request, "Cannot delete supplier because it is in use.")
            return redirect("supplier_list")

class SupplierProductListView(ListView):
    model = SupplierProduct
    template_name = "list_base.html"
    context_object_name = "rows"

    def get_queryset(self):
        return SupplierProduct.objects.filter(supplier_id=self.kwargs["supplier_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        supplier_id = self.kwargs["supplier_id"]

        supplier = get_object_or_404(Supplier, pk=supplier_id)

        context.update({
            "title": f"Products supplied by {supplier.name}",
            "columns": ["product", "cost_price", "lead_time_days"],
            "top_header": None,
            "parent_header": RecordHeader(
                title=supplier.name,
                fields={
                    "Email": supplier.email or "—",
                    "Phone": supplier.phone or "—",
                },
            ),

            # /supppliers
            "back_builder": UrlBuilder(
                "supplier_list",
                [] 
            ),
            
            # /suppliers/<supplier_id>/products/new/
            "new_builder": UrlBuilder(
                "supplier_product_create",
                ["supplier_id"]  # pk = supplier_id from URL kwargs
            ),

            # /suppliers/<supplier_id>/products/<supplierproduct_id>/edit/
            "edit_builder": UrlBuilder(
                "supplier_product_edit",
                ["supplier_id", "pk"]  # supplier_id, then the supplierproduct.id from row
            ),

            # /suppliers/<supplier_id>/products/<supplierproduct_id>/delete/
            "delete_builder": UrlBuilder(
                "supplier_product_delete",
                ["supplier_id", "pk"]
            ),
        })

        return context

class SupplierProductCreateView(CreateView):
    model = SupplierProduct
    form_class = SupplierProductForm
    template_name = "form_base.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["supplier_id"] = self.kwargs["supplier_id"]
        return kwargs
    
    def form_valid(self, form):
        form.instance.supplier_id = self.kwargs["supplier_id"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("supplier_products", args=[self.kwargs["supplier_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Supplier Product"
        context["cancel_url"] = reverse_lazy("supplier_products", args=[self.kwargs["supplier_id"]])
        return context


class SupplierProductUpdateView(UpdateView):
    model = SupplierProduct
    form_class = SupplierProductForm
    template_name = "form_base.html"

    pk_url_kwarg = "supplier_product_id"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["supplier_id"] = self.kwargs["supplier_id"]
        return kwargs
    
    def form_valid(self, form):
        form.instance.supplier_id = self.kwargs["supplier_id"]
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("supplier_products", args=[self.kwargs["supplier_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Supplier Product"
        context["cancel_url"] = reverse_lazy("supplier_products", args=[self.kwargs["supplier_id"]])
        return context


class SupplierProductDeleteView(DeleteView):
    model = SupplierProduct
    template_name = "confirm_delete.html"

    pk_url_kwarg = "supplier_product_id"

    def get_success_url(self):
        return reverse_lazy("supplier_products", args=[self.kwargs["supplier_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Remove Product From Supplier"
        context["cancel_url"] = reverse_lazy("supplier_products", args=[self.kwargs["supplier_id"]])
        return context