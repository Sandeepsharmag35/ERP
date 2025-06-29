from django import forms
from django.forms import ModelForm
from .models import Warehouse, InventoryLocation, InventoryItem, InventoryTransaction


class WarehouseForm(ModelForm):
    class Meta:
        model = Warehouse
        fields = ["user", "organization", "code", "name", "address", "is_active"]
        widgets = {
            "user": forms.Select(
                attrs={
                    "class": "mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                }
            ),
            "organization": forms.Select(
                attrs={
                    "class": "mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                }
            ),
            "code": forms.TextInput(
                attrs={
                    "class": "mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                    "placeholder": "Enter warehouse code",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                    "placeholder": "Enter warehouse name",
                }
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                    "rows": 3,
                    "placeholder": "Enter warehouse address",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                }
            ),
        }


class InventoryLocationForm(ModelForm):
    class Meta:
        model = InventoryLocation
        fields = [
            "user",
            "organization",
            "warehouse",
            "code",
            "name",
            "location_type",
            "is_active",
        ]
        widgets = {
            "user": forms.Select(
                attrs={
                    "class": "mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                }
            ),
            "organization": forms.Select(
                attrs={
                    "class": "mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                }
            ),
            "warehouse": forms.Select(
                attrs={
                    "class": "mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                }
            ),
            "code": forms.TextInput(
                attrs={
                    "class": "mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                    "placeholder": "Enter location code",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                    "placeholder": "Enter location name",
                }
            ),
            "location_type": forms.TextInput(
                attrs={
                    "class": "mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                    "placeholder": "e.g., aisle, bin, shelf",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                }
            ),
        }


class InventoryTransactionForm(ModelForm):
    class Meta:
        model = InventoryTransaction
        fields = [
            "user",
            "organization",
            "transaction_type",
            "product",
            "from_warehouse",
            "to_warehouse",
            "quantity",
            "unit_cost",
        ]
        widgets = {
            "user": forms.Select(
                attrs={
                    "class": "mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                }
            ),
            "organization": forms.Select(
                attrs={
                    "class": "mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                }
            ),
            "transaction_type": forms.Select(
                attrs={
                    "class": "mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                    "hx-get": "/inventory/transaction-fields/",
                    "hx-target": "#warehouse-fields",
                    "hx-trigger": "change",
                }
            ),
            "product": forms.Select(
                attrs={
                    "class": "mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                }
            ),
            "from_warehouse": forms.Select(
                attrs={
                    "class": "mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                }
            ),
            "to_warehouse": forms.Select(
                attrs={
                    "class": "mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "unit_cost": forms.NumberInput(
                attrs={
                    "class": "mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                    "step": "0.0001",
                    "min": "0",
                }
            ),
        }


class StockFilterForm(forms.Form):
    warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.filter(is_active=True),
        required=False,
        empty_label="All Warehouses",
        widget=forms.Select(
            attrs={
                "class": "px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                "hx-get": "/inventory/stock/",
                "hx-target": "#stock-grid",
                "hx-trigger": "change",
                "hx-include": "#filter-form",
            }
        ),
    )

    location = forms.ModelChoiceField(
        queryset=InventoryLocation.objects.filter(is_active=True),
        required=False,
        empty_label="All Locations",
        widget=forms.Select(
            attrs={
                "class": "px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                "hx-get": "/inventory/stock/",
                "hx-target": "#stock-grid",
                "hx-trigger": "change",
                "hx-include": "#filter-form",
            }
        ),
    )

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                "placeholder": "Search products...",
                "hx-get": "/inventory/stock/",
                "hx-target": "#stock-grid",
                "hx-trigger": "keyup changed delay:500ms",
                "hx-include": "#filter-form",
            }
        ),
    )
