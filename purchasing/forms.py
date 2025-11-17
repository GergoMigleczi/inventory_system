from django import forms
from django.forms import inlineformset_factory
from .models import PurchaseOrder, PurchaseOrderLine, GoodsReceipt, GoodsReceiptLine

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ["supplier", "warehouse", "ordered_at", "expected_at", "status", "reference"]
        widgets = {
            "supplier": forms.Select(attrs={"class": "form-control"}),
            "warehouse": forms.Select(attrs={"class": "form-control"}),
            "ordered_at": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "expected_at": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "reference": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Editing an existing PO?
        if self.instance and self.instance.pk:
            if self.instance.status != "draft":
                # Disable all fields except status field (status transitions will be done outside this form)
                for field_name in ["supplier", "warehouse", "ordered_at", "expected_at", "reference"]:
                    self.fields[field_name].disabled = True

class PurchaseOrderLineForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderLine
        fields = ["product", "quantity", "unit_price"]
        widgets = {
            "product": forms.Select(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "unit_price": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, purchase_order_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.purchase_order_id = purchase_order_id

        # Assign FK here so model.clean() has it before validation
        if purchase_order_id and not self.instance.pk:
            self.instance.purchase_order_id = purchase_order_id

        # If editing and PO is not draft → disable fields
        if self.instance and self.instance.pk:
            po = self.instance.purchase_order
            if po.status != "draft":
                for field in self.fields.values():
                    field.disabled = True



class GoodsReceiptForm(forms.ModelForm):
    class Meta:
        model = GoodsReceipt
        fields = ["purchase_order", "supplier", "warehouse", "received_at", "status", "reference"]
        widgets = {
            "purchase_order": forms.Select(attrs={"class": "form-control"}),
            "supplier": forms.Select(attrs={"class": "form-control"}),
            "warehouse": forms.Select(attrs={"class": "form-control"}),
            "received_at": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "reference": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Editing an existing GRV?
        if self.instance and self.instance.pk:
            if self.instance.status != "draft":
                # Disable all fields except status field (status transitions will be done outside this form)
                for field_name in ["purchase_order", "supplier", "warehouse", "received_at", "reference"]:
                    self.fields[field_name].disabled = True

class GoodsReceiptLineForm(forms.ModelForm):
    class Meta:
        model = GoodsReceiptLine
        fields = ["product", "quantity",  "expiry_date", "unit_price"]
        widgets = {
            "product": forms.Select(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "expiry_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "unit_price": forms.NumberInput(attrs={"class": "form-control"})            
        }

    def __init__(self, *args, goods_receipt_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.goods_receipt_id = goods_receipt_id

        # Assign FK here so model.clean() has it before validation
        if goods_receipt_id and not self.instance.pk:
            self.instance.goods_receipt_id = goods_receipt_id

        # If editing and PO is not draft → disable fields
        if self.instance and self.instance.pk:
            grv = self.instance.goods_receipt
            if grv.status != "draft":
                for field in self.fields.values():
                    field.disabled = True
