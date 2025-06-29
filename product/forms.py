from django import forms
from .models import Product, Uom, ProductUom


class UomForm(forms.ModelForm):
    class Meta:
        model = Uom
        fields = ["user", "organization", "code", "name", "category", "conversion_to_si"]
        widgets = {
            "user": forms.Select(
                attrs={
                    "class": "mt-1 p-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                }
            ),
            "organization": forms.Select(
                attrs={
                    "class": "mt-1 p-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                }
            ),
            "code": forms.TextInput(
                attrs={
                    "class": "mt-1 p-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
                    "placeholder": "e.g., EA, KG, M",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "mt-1 p-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
                    "placeholder": "e.g., Each, Kilogram, Meter",
                }
            ),
            "category": forms.TextInput(
                attrs={
                    "class": "mt-1 p-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
                    "placeholder": "e.g., weight, length, qty",
                }
            ),
            "conversion_to_si": forms.NumberInput(
                attrs={
                    "class": "mt-1 p-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
                    "step": "0.0001",
                    "placeholder": "1.0000",
                }
            ),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "user",
            "organization",
            "product_code",
            "name",
            "base_uom",
            "costing_method",
            "tracking_method",
            "safety_stock",
            "reorder_qty",
            "is_active",
        ]
        widgets = {
            "user": forms.Select(
                attrs={
                    "class": "mt-1 p-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                }
            ),
            "organization": forms.Select(
                attrs={
                    "class": "mt-1 p-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                }
            ),
            "product_code": forms.TextInput(
                attrs={
                    "class": "mt-1 p-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
                    "placeholder": "Product code",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "mt-1 p-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
                    "placeholder": "Product name",
                }
            ),
            "base_uom": forms.Select(
                attrs={
                    "class": "mt-1 p-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                }
            ),
            "costing_method": forms.Select(
                attrs={
                    "class": "mt-1 p-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                }
            ),
            "tracking_method": forms.Select(
                attrs={
                    "class": "mt-1 p-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                }
            ),
            "safety_stock": forms.NumberInput(
                attrs={
                    "class": "mt-1 p-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "reorder_qty": forms.NumberInput(
                attrs={
                    "class": "mt-1 p-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "h-4 w-4 p-2 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["base_uom"].queryset = Uom.objects.all()


class ProductUomForm(forms.ModelForm):
    class Meta:
        model = ProductUom
        fields = ["uom", "factor", "is_default_sales", "is_default_purchase"]
        widgets = {
            "uom": forms.Select(
                attrs={
                    "class": "mt-1 p-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                }
            ),
            "factor": forms.NumberInput(
                attrs={
                    "class": "mt-1 p-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
                    "step": "0.0001",
                    "min": "0.0001",
                }
            ),
            "is_default_sales": forms.CheckboxInput(
                attrs={
                    "class": "h-4 w-4 p-2 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                }
            ),
            "is_default_purchase": forms.CheckboxInput(
                attrs={
                    "class": "h-4 w-4 p-2 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["uom"].queryset = Uom.objects.all()
