from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from .forms import PurchaseOrderForm, PurchaseOrderLineForm, GoodsReceiptForm, GoodsReceiptLineForm
from .models import PurchaseOrder, PurchaseOrderLine, GoodsReceipt, GoodsReceiptLine
from inventory_system.utils.urlbuilder import UrlBuilder
from inventory_system.utils.recordheader import RecordHeader


class PurchaseOrderListView(ListView):
    model = PurchaseOrder
    template_name = "list_base.html"
    context_object_name = "rows"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "title": "Purchase Orders",
            "columns": ["number", "supplier", "warehouse", "ordered_at", "expected_at", "status", "reference"],
            "new_builder": UrlBuilder("purchase_order_create", []),
            "edit_builder": UrlBuilder("purchase_order_edit", ["pk"]),
            "delete_builder": UrlBuilder("purchase_order_delete", ["pk"]),
            "extra_actions": [
                {
                    "label": "Line Items",
                    "builder": UrlBuilder("purchase_order_line_items", ["pk"]),
                },
                {
                    "label": "Create GRV",
                    "builder": UrlBuilder("goods_receipt_create", [], {"po": "pk"}),
                },
            ],
        })

        return context


class PurchaseOrderCreateView(CreateView):
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = "form_base.html"
    success_url = reverse_lazy("purchase_order_list")

    extra_context = {
        "title": "Open Purchase Order",
        "cancel_url": reverse_lazy("purchase_order_list"),
    }


class PurchaseOrderUpdateView(UpdateView):
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = "form_base.html"

    pk_url_kwarg = "purchase_order_id"
    success_url = reverse_lazy("purchase_order_list")

    extra_context = {
        "title": "Edit Purchase Order",
        "cancel_url": reverse_lazy("purchase_order_list"),
    }

class PurchaseOrderDeleteView(DeleteView):
    model = PurchaseOrder
    template_name = "confirm_delete.html"

    pk_url_kwarg = "purchase_order_id"
    success_url = reverse_lazy("purchase_order_list")

    extra_context = {
        "title": "Delete Purchase Order",
        "cancel_url": reverse_lazy("purchase_order_list"),
    }

    def dispatch(self, request, *args, **kwargs):
        po = self.get_object()
        if po.status != "draft":
            messages.error(request, "Cannot delete a purchase order unless it is in Draft status.")
            return redirect("purchase_order_list")
        return super().dispatch(request, *args, **kwargs)


class PurchaseOrderLineListView(ListView):
    model = PurchaseOrderLine
    template_name = "list_base.html"
    context_object_name = "rows"

    def get_queryset(self):
        return PurchaseOrderLine.objects.filter(purchase_order_id=self.kwargs["purchase_order_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchase_order_id = self.kwargs["purchase_order_id"]

        po = get_object_or_404(PurchaseOrder, pk=purchase_order_id)

        context.update({
            "title": f"{po.number} Line Items",
            "columns": ["product", "quantity", "unit_price"],
            "top_header": None,
            "parent_header": RecordHeader(
                title=po.number,
                fields={
                    "Status": po.status or "—",
                    "Ordered at": po.ordered_at or "—",
                    "Expected at": po.expected_at or "—",
                    "Supplier": po.supplier or "—",
                    "Receiving Warehouse": po.warehouse or "—",
                },
            ),

            "back_builder": UrlBuilder("purchase_order_list",[]),
            
            "new_builder": UrlBuilder("purchase_order_line_create", ["purchase_order_id"]),

            "edit_builder": UrlBuilder("purchase_order_line_edit", ["purchase_order_id", "pk"]),

            "delete_builder": UrlBuilder("purchase_order_line_delete", ["purchase_order_id", "pk"]),
        })

        return context

class PurchaseOrderLineCreateView(CreateView):
    model = PurchaseOrderLine
    form_class = PurchaseOrderLineForm
    template_name = "form_base.html"

    def dispatch(self, request, *args, **kwargs):
        po = get_object_or_404(PurchaseOrder, pk=self.kwargs["purchase_order_id"])
        if po.status != "draft":
            messages.error(request, "Cannot add line items unless PO is in Draft status.")
            return redirect("purchase_order_line_items", purchase_order_id=self.kwargs["purchase_order_id"])

        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["purchase_order_id"] = self.kwargs["purchase_order_id"]
        return kwargs
    
    def form_valid(self, form):
        form.instance.purchase_order_id = self.kwargs["purchase_order_id"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("purchase_order_line_items", args=[self.kwargs["purchase_order_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add PO Line Item"
        context["cancel_url"] = reverse_lazy("purchase_order_line_items", args=[self.kwargs["purchase_order_id"]])
        return context


class PurchaseOrderLineUpdateView(UpdateView):
    model = PurchaseOrderLine
    form_class = PurchaseOrderLineForm
    template_name = "form_base.html"

    pk_url_kwarg = "purchase_order_line_id"

    def dispatch(self, request, *args, **kwargs):
        line = self.get_object()
        if line.purchase_order.status != "draft":
            messages.error(request, "Cannot edit line items unless PO is in Draft status.")
            return redirect("purchase_order_line_items", purchase_order_id=self.kwargs["purchase_order_id"])
        
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["purchase_order_id"] = self.kwargs["purchase_order_id"]
        return kwargs
    
    def form_valid(self, form):
        form.instance.purchase_order_id = self.kwargs["purchase_order_id"]
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("purchase_order_line_items", args=[self.kwargs["purchase_order_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit PO Line Item"
        context["cancel_url"] = reverse_lazy("purchase_order_line_items", args=[self.kwargs["purchase_order_id"]])
        return context


class PurchaseOrderLineDeleteView(DeleteView):
    model = PurchaseOrderLine
    template_name = "confirm_delete.html"

    pk_url_kwarg = "purchase_order_line_id"

    def dispatch(self, request, *args, **kwargs):
        line = self.get_object()
        if line.purchase_order.status != "draft":
            messages.error(request, "Cannot delete line items unless PO is in Draft status.")
            return redirect("purchase_order_line_items", purchase_order_id=self.kwargs["purchase_order_id"])

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("purchase_order_line_items", args=[self.kwargs["purchase_order_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Remove Line Item From PO"
        context["cancel_url"] = reverse_lazy("purchase_order_line_items", args=[self.kwargs["purchase_order_id"]])
        return context
    

class GoodsReceiptListView(ListView):
    model = GoodsReceipt
    template_name = "list_base.html"
    context_object_name = "rows"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "title": "Goods Receiving Vouchers",
            "columns": ["number", "purchase_order", "supplier", "warehouse", "received_at", "status", "reference", "created_by"],
            "new_builder": UrlBuilder("goods_receipt_create", []),
            "edit_builder": UrlBuilder("goods_receipt_edit", ["pk"]),
            "delete_builder": UrlBuilder("goods_receipt_delete", ["pk"]),
            "extra_actions": [
                {
                    "label": "Line Items",
                    "builder": UrlBuilder("goods_receipt_line_items", ["pk"]),
                }
            ],
        })

        return context


class GoodsReceiptCreateView(CreateView):
    model = GoodsReceipt
    form_class = GoodsReceiptForm
    template_name = "form_base.html"

    def get_initial(self):
        """
        Auto-populate GRV header fields when ?po=<id> is provided.
        """
        initial = super().get_initial()
        po_id = self.request.GET.get("po")

        if po_id:
            try:
                po = PurchaseOrder.objects.get(pk=po_id)

                # Only allow submitted POs to be received
                if po.status != "submitted":
                    messages.error(
                        self.request,
                        "This purchase order is not in 'Submitted' status and cannot be received."
                    )
                    return initial

                initial["purchase_order"] = po
                initial["supplier"] = po.supplier
                initial["warehouse"] = po.warehouse

            except PurchaseOrder.DoesNotExist:
                pass  # invalid id = ignore and leave blank

        return initial

    def form_valid(self, form):
        """
        1. Save GRV header
        2. Auto-generate GRV lines based on PO outstanding quantities
        """
        grv = form.save(commit=False)
        grv.created_by = self.request.user
        po = grv.purchase_order

        # Validate the PO status
        if po.status != "submitted":
            messages.error(self.request, "Only submitted purchase orders can be received.")
            return redirect("goods_receipt_list")

        # Save header first
        grv.save()

        # Auto-create GRV lines
        for po_line in po.lines.all():
            outstanding = po_line.outstanding_for_grv()

            if outstanding > 0:
                GoodsReceiptLine.objects.create(
                    goods_receipt=grv,
                    purchase_order_line=po_line,
                    product=po_line.product,
                    quantity=outstanding,
                    unit_price=po_line.unit_price,
                )

        messages.success(self.request, "Goods receipt created. Set expiry dates, then close the GRV.")
        
        # This will now call get_success_url()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("goods_receipt_line_items", args=[self.object.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Goods Receiving Voucher"
        context["cancel_url"] = reverse_lazy("goods_receipt_list")
        return context

class GoodsReceiptUpdateView(UpdateView):
    model = GoodsReceipt
    form_class = GoodsReceiptForm
    template_name = "form_base.html"

    pk_url_kwarg = "goods_receipt_id"
    success_url = reverse_lazy("goods_receipt_list")

    extra_context = {
        "title": "Edit Goods Receiving Voucher",
        "cancel_url": reverse_lazy("goods_receipt_list"),
    }

    def dispatch(self, request, *args, **kwargs):
        grv = self.get_object()
        if grv.status != "draft":
            messages.error(request, "Cannot update a goods receiving voucher unless it is in Draft status.")
            return redirect("goods_receipt_list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        old_status = self.object.status  # status BEFORE edit

        response = super().form_valid(form)  # saves object, triggers model.clean() + model.save()
        grv = self.object                # easier alias

        # Detect if GRV was closed
        if old_status != "closed" and grv.status == "closed":
            messages.success(self.request, "Goods Receipt closed and inventory updated.")

            # Check if PO was also closed
            if grv.purchase_order and grv.purchase_order.status == "received":
                messages.info(
                    self.request,
                    f"Purchase Order {grv.purchase_order.number} has also been closed."
                )

        return response


class GoodsReceiptDeleteView(DeleteView):
    model = GoodsReceipt
    template_name = "confirm_delete.html"

    pk_url_kwarg = "goods_receipt_id"
    success_url = reverse_lazy("goods_receipt_list")

    extra_context = {
        "title": "Delete Goods Receiving Voucher",
        "cancel_url": reverse_lazy("goods_receipt_list"),
    }

    def dispatch(self, request, *args, **kwargs):
        grv = self.get_object()
        if grv.status != "draft":
            messages.error(request, "Cannot delete a goods receiving voucher unless it is in Draft status.")
            return redirect("goods_receipt_list")
        return super().dispatch(request, *args, **kwargs)


class GoodsReceiptLineListView(ListView):
    model = GoodsReceiptLine
    template_name = "list_base.html"
    context_object_name = "rows"

    def get_queryset(self):
        return GoodsReceiptLine.objects.filter(goods_receipt_id=self.kwargs["goods_receipt_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        goods_receipt_id = self.kwargs["goods_receipt_id"]

        grv = get_object_or_404(GoodsReceipt, pk=goods_receipt_id)

        context.update({
            "title": f"{grv.number} Line Items",
            "columns": ["product", "quantity", "expiry_date", "unit_price"],
            "top_header": None,
            "parent_header": RecordHeader(
                title=grv.number,
                fields={
                    "Status": grv.status or "—",
                    "Received at": grv.received_at or "—",
                    "Linked PO": grv.purchase_order or "—",
                    "Supplier": grv.supplier or "—",
                    "Receiving Warehouse": grv.warehouse or "—",
                },
            ),

            "back_builder": UrlBuilder("goods_receipt_list",[]),
            
            "new_builder": UrlBuilder("goods_receipt_line_create", ["goods_receipt_id"]),

            "edit_builder": UrlBuilder("goods_receipt_line_edit", ["goods_receipt_id", "pk"]),

            "delete_builder": UrlBuilder("goods_receipt_line_delete", ["goods_receipt_id", "pk"]),
        })

        return context

class GoodsReceiptLineCreateView(CreateView):
    model = GoodsReceiptLine
    form_class = GoodsReceiptLineForm
    template_name = "form_base.html"

    def dispatch(self, request, *args, **kwargs):
        grv = get_object_or_404(GoodsReceipt, pk=self.kwargs["goods_receipt_id"])
        if grv.status != "draft":
            messages.error(request, "Cannot add line items unless GRV is in Draft status.")
            return redirect("goods_receipt_line_items", goods_receipt_id=self.kwargs["goods_receipt_id"])

        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["goods_receipt_id"] = self.kwargs["goods_receipt_id"]
        return kwargs
    
    def form_valid(self, form):
        form.instance.goods_receipt_id = self.kwargs["goods_receipt_id"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("goods_receipt_line_items", args=[self.kwargs["goods_receipt_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add GRV Line Item"
        context["cancel_url"] = reverse_lazy("goods_receipt_line_items", args=[self.kwargs["goods_receipt_id"]])
        return context


class GoodsReceiptLineUpdateView(UpdateView):
    model = GoodsReceiptLine
    form_class = GoodsReceiptLineForm
    template_name = "form_base.html"

    pk_url_kwarg = "goods_receipt_line_id"

    def dispatch(self, request, *args, **kwargs):
        line = self.get_object()
        if line.goods_receipt.status != "draft":
            messages.error(request, "Cannot edit line items unless GRV is in Draft status.")
            return redirect("goods_receipt_line_items", goods_receipt_id=self.kwargs["goods_receipt_id"])
        
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["goods_receipt_id"] = self.kwargs["goods_receipt_id"]
        return kwargs
    
    def form_valid(self, form):
        form.instance.goods_receipt_id = self.kwargs["goods_receipt_id"]
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("goods_receipt_line_items", args=[self.kwargs["goods_receipt_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit GRV Line Item"
        context["cancel_url"] = reverse_lazy("goods_receipt_line_items", args=[self.kwargs["goods_receipt_id"]])
        return context


class GoodsReceiptLineDeleteView(DeleteView):
    model = GoodsReceiptLine
    template_name = "confirm_delete.html"

    pk_url_kwarg = "goods_receipt_line_id"

    def dispatch(self, request, *args, **kwargs):
        line = self.get_object()
        if line.goods_receipt.status != "draft":
            messages.error(request, "Cannot delete line items unless GRV is in Draft status.")
            return redirect("goods_receipt_line_items", goods_receipt_id=self.kwargs["goods_receipt_id"])

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("goods_receipt_line_items", args=[self.kwargs["goods_receipt_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Remove Line Item From GRV"
        context["cancel_url"] = reverse_lazy("goods_receipt_line_items", args=[self.kwargs["goods_receipt_id"]])
        return context
    

