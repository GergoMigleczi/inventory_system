from django import forms
from .models import Supplier, SupplierProduct


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "email", "phone", "contact_name", "address_line1",
                  "address_line2", "city", "postcode", "country", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "contact_name": forms.TextInput(attrs={"class": "form-control"}),
            "address_line1": forms.TextInput(attrs={"class": "form-control"}),
            "address_line2": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "postcode": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

class SupplierProductForm(forms.ModelForm):
    class Meta:
        model = SupplierProduct
        fields = ["product", "cost_price", "lead_time_days"]
        widgets = {
            "product": forms.Select(attrs={"class": "form-control"}),
            "cost_price": forms.NumberInput(attrs={"class": "form-control"}),
            "lead_time_days": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, supplier_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.supplier_id = supplier_id

        # Disable product when editing
        if self.instance.pk:
            self.fields["product"].disabled = True

    def clean(self):
        cleaned = super().clean()

        supplier_id = self.supplier_id
        product = cleaned.get("product")

        if not supplier_id or not product:
            return cleaned

        # Creating a new entry
        if not self.instance.pk:
            if SupplierProduct.objects.filter(
                supplier_id=supplier_id,
                product=product
            ).exists():
                raise forms.ValidationError(
                    "This supplier already provides this product."
                )
            return cleaned

        # Updating an existing entry — ignore current object
        if SupplierProduct.objects.filter(
            supplier_id=supplier_id,
            product=product
        ).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                "This supplier already provides this product."
            )

        return cleaned
