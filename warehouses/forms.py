from django import forms
from .models import Warehouse, ProductBatch


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ["name", "location"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
        }


class ProductBatchForm(forms.ModelForm):
    class Meta:
        model = ProductBatch
        fields = ['lot_number', 'product', 'quantity', 'expiry_date']
        widgets = {
            'lot_number': forms.TextInput(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, warehouse_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.warehouse_id = warehouse_id

        # If editing an existing batch
        if self.instance and self.instance.pk:
            # Disable product, warehouse, lot_number
            self.fields['product'].disabled = True
            self.fields['lot_number'].disabled = True

