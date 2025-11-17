from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Warehouse, ProductBatch
from .forms import WarehouseForm, ProductBatchForm
from django.shortcuts import get_object_or_404
from inventory_system.utils.urlbuilder import UrlBuilder
from inventory_system.utils.recordheader import RecordHeader

class WarehouseListView(ListView):
    model = Warehouse
    template_name = "list_base.html"
    context_object_name = "rows"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "title": "Warehouses",
            "columns": ["name", "location"],
            "new_builder": UrlBuilder("warehouse_create", []),
            "edit_builder": UrlBuilder("warehouse_edit", ["pk"]),
            "delete_builder": UrlBuilder("warehouse_delete", ["pk"]),
            "extra_actions": [
                {
                    "label": "Inventory",
                    # /warehouses/<id>/batches/
                    "builder": UrlBuilder("warehouse_batches", ["pk"]),
                }
            ],
        })

        return context



class WarehouseCreateView(CreateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = "form_base.html"
    success_url = reverse_lazy("warehouse_list")

    extra_context = {
        "title": "Add Warehouse",
        "cancel_url": reverse_lazy("warehouse_list"),
    }


class WarehouseUpdateView(UpdateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = "form_base.html"
    pk_url_kwarg = "warehouse_id"
    success_url = reverse_lazy("warehouse_list")

    extra_context = {
        "title": "Edit Warehouse",
        "cancel_url": reverse_lazy("warehouse_list"),
    }

class WarehouseDeleteView(DeleteView):
    model = Warehouse
    template_name = "confirm_delete.html"
    pk_url_kwarg = "warehouse_id"
    success_url = reverse_lazy("warehouse_list")

    extra_context = {
        "title": "Delete Warehouse",
        "cancel_url": reverse_lazy("warehouse_list"),
    }
class ProductBatchListView(ListView):
    model = ProductBatch
    template_name = "list_base.html"
    context_object_name = "rows"

    def get_queryset(self):
        return ProductBatch.objects.filter(
            warehouse_id=self.kwargs["warehouse_id"]
        ).select_related("product", "warehouse")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        warehouse_id = self.kwargs["warehouse_id"]

        warehouse = get_object_or_404(Warehouse, pk=warehouse_id)

        context.update({
            "title": f"Products in {warehouse.name}",
            "columns": ["goods_receipt_line", "product", "quantity", "expiry_date"],
            "top_header": None,
            "parent_header": RecordHeader(
                title=warehouse.name,
                fields={
                    "Location": warehouse.location or "—",
                },
            ),

            # /warehouses
            "back_builder": UrlBuilder(
                "warehouse_list",
                [] 
            ),

            # /warehouses/<warehouse_id>/batches/new/
            "new_builder": UrlBuilder(
                "warehouse_batch_create",
                ["warehouse_id"] 
            ),

            # /warehouses/<warehouse_id>/batches/<batch_id>/edit/
            "edit_builder": UrlBuilder(
                "warehouse_batch_edit",
                ["warehouse_id", "pk"]
            ),

            # /warehouses/<warehouse_id>/batches/<batch_id>/delete/
            "delete_builder": UrlBuilder(
                "warehouse_batch_delete",
                ["warehouse_id", "pk"]
            ),
        })

        return context


class ProductBatchCreateView(CreateView):
    model = ProductBatch
    form_class = ProductBatchForm
    template_name = "form_base.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["warehouse_id"] = self.kwargs["warehouse_id"]
        return kwargs
    
    def form_valid(self, form):
        form.instance.warehouse_id = self.kwargs["warehouse_id"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("warehouse_batches", kwargs={"warehouse_id": self.kwargs["warehouse_id"]})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Warehouse Batch"
        context["cancel_url"] = reverse_lazy("warehouse_batches", args=[self.kwargs["warehouse_id"]])
        return context



class ProductBatchUpdateView(UpdateView):
    model = ProductBatch
    form_class = ProductBatchForm
    template_name = "form_base.html"
    pk_url_kwarg = "batch_id"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["warehouse_id"] = self.kwargs["warehouse_id"]
        return kwargs
    
    def form_valid(self, form):
        form.instance.warehouse_id = self.kwargs["warehouse_id"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("warehouse_batches", kwargs={"warehouse_id": self.kwargs["warehouse_id"]})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Warehouse Batch"
        context["cancel_url"] = reverse_lazy("warehouse_batches", args=[self.kwargs["warehouse_id"]])
        return context


class ProductBatchDeleteView(DeleteView):
    model = ProductBatch
    template_name = "confirm_delete.html"
    pk_url_kwarg = "batch_id"

    def get_success_url(self):
        return reverse_lazy("warehouse_batches", kwargs={"warehouse_id": self.kwargs["warehouse_id"]})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Warehouse Batch"
        context["cancel_url"] = reverse_lazy("warehouse_batches", args=[self.kwargs["warehouse_id"]])
        return context
