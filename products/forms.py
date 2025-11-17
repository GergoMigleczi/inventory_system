from django import forms
from .models import Category, UnitOfMeasure, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "parent"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "parent": forms.Select(attrs={"class": "form-control"}),
        }

class UnitsOfMeasureForm(forms.ModelForm):
    class Meta:
        model = UnitOfMeasure
        fields = ["short_code", "name"]
        widgets = {
            "short_code": forms.TextInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["sku", "name", "description", "category", "unit", "active"]
        widgets = {
            "sku": forms.TextInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "unit": forms.Select(attrs={"class": "form-control"}),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
