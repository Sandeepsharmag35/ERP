from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Warehouse, InventoryLocation, InventoryItem, InventoryTransaction
from .forms import (
    WarehouseForm,
    InventoryLocationForm,
    InventoryTransactionForm,
    StockFilterForm,
)
import json


def warehouse_list(request):
    """List warehouses with optional JSON response"""
    warehouses = Warehouse.objects.filter(is_active=True).order_by("name")

    if request.headers.get("Accept") == "application/json":
        data = [
            {
                "warehouse_id": str(w.warehouse_id),
                "code": w.code,
                "name": w.name,
                "address": w.address,
            }
            for w in warehouses
        ]
        return JsonResponse({"warehouses": data})

    context = {"warehouses": warehouses, "form": WarehouseForm()}
    return render(request, "inventory/warehouse_list.html", context)


@require_http_methods(["POST"])
def warehouse_create(request):
    """Create new warehouse"""
    form = WarehouseForm(request.POST)

    if form.is_valid():
        warehouse = form.save()
        messages.success(request, f'Warehouse "{warehouse.name}" created successfully!')

        if request.headers.get("HX-Request"):
            # Return updated warehouse list for HTMX
            warehouses = Warehouse.objects.filter(is_active=True).order_by("name")
            return render(
                request,
                "inventory/partials/warehouse_list.html",
                {"warehouses": warehouses},
            )

        return redirect("warehouse_list")

    if request.headers.get("HX-Request"):
        return render(request, "inventory/partials/warehouse_form.html", {"form": form})

    warehouses = Warehouse.objects.filter(is_active=True).order_by("name")
    return render(
        request,
        "inventory/warehouse_list.html",
        {"warehouses": warehouses, "form": form},
    )


def stock_grid(request):
    """Display stock on-hand with filters"""
    form = StockFilterForm(request.GET)

    # Base queryset
    queryset = InventoryItem.objects.select_related(
        "product", "warehouse", "location"
    ).filter(quantity_on_hand__gt=0)

    # Apply filters
    if form.is_valid():
        if form.cleaned_data.get("warehouse"):
            queryset = queryset.filter(warehouse=form.cleaned_data["warehouse"])

        if form.cleaned_data.get("location"):
            queryset = queryset.filter(location=form.cleaned_data["location"])

        if form.cleaned_data.get("search"):
            search_term = form.cleaned_data["search"]
            queryset = queryset.filter(
                Q(product__name__icontains=search_term)
                | Q(warehouse__code__icontains=search_term)
                | Q(location__code__icontains=search_term)
            )

    # Pagination
    paginator = Paginator(queryset.order_by("product__name"), 25)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "form": form,
        "page_obj": page_obj,
        "inventory_items": page_obj.object_list,
    }

    if request.headers.get("HX-Request"):
        return render(request, "inventory/partials/stock_grid.html", context)

    return render(request, "inventory/stock_grid.html", context)


@require_http_methods(["GET", "POST"])
def stock_movement_create(request):
    """Create inventory transaction"""
    if request.method == "POST":
        form = InventoryTransactionForm(request.POST)

        if form.is_valid():
            transaction = form.save()

            response_data = {
                "transaction_id": str(transaction.transaction_id),
                "success": True,
                "message": f"Transaction {transaction.transaction_type} created successfully",
            }

            if request.headers.get("HX-Request"):
                messages.success(request, response_data["message"])
                return render(
                    request,
                    "inventory/partials/transaction_success.html",
                    {"transaction": transaction},
                )

            return JsonResponse(response_data, status=201)

        if request.headers.get("HX-Request"):
            return render(
                request, "inventory/partials/transaction_form.html", {"form": form}
            )

        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    # GET request
    form = InventoryTransactionForm()
    return render(request, "inventory/stock_movement.html", {"form": form})


def transaction_fields_partial(request):
    """Return warehouse fields based on transaction type"""
    transaction_type = request.GET.get("transaction_type")

    context = {
        "transaction_type": transaction_type,
        "warehouses": Warehouse.objects.filter(is_active=True),
    }

    return render(request, "inventory/partials/warehouse_fields.html", context)


def warehouse_detail(request, warehouse_id):
    """Display warehouse details with locations"""
    warehouse = get_object_or_404(Warehouse, warehouse_id=warehouse_id)
    locations = InventoryLocation.objects.filter(
        warehouse=warehouse, is_active=True
    ).order_by("code")

    context = {
        "warehouse": warehouse,
        "locations": locations,
        "location_form": InventoryLocationForm(initial={"warehouse": warehouse}),
    }

    return render(request, "inventory/warehouse_detail.html", context)


@require_http_methods(["POST"])
def location_create(request, warehouse_id):
    """Create new inventory location"""
    warehouse = get_object_or_404(Warehouse, warehouse_id=warehouse_id)
    form = InventoryLocationForm(request.POST)

    if form.is_valid():
        location = form.save()
        messages.success(request, f'Location "{location.name}" created successfully!')

        if request.headers.get("HX-Request"):
            locations = InventoryLocation.objects.filter(
                warehouse=warehouse, is_active=True
            ).order_by("code")
            return render(
                request,
                "inventory/partials/location_list.html",
                {"locations": locations, "warehouse": warehouse},
            )

        return redirect("warehouse_detail", warehouse_id=warehouse_id)

    if request.headers.get("HX-Request"):
        return render(
            request,
            "inventory/partials/location_form.html",
            {"form": form, "warehouse": warehouse},
        )

    return redirect("warehouse_detail", warehouse_id=warehouse_id)


def dashboard(request):
    """Inventory dashboard with key metrics"""
    total_warehouses = Warehouse.objects.filter(is_active=True).count()
    total_locations = InventoryLocation.objects.filter(is_active=True).count()
    total_items = InventoryItem.objects.filter(quantity_on_hand__gt=0).count()

    recent_transactions = InventoryTransaction.objects.select_related(
        "product", "from_warehouse", "to_warehouse"
    ).order_by("-transaction_date")[:10]

    context = {
        "total_warehouses": total_warehouses,
        "total_locations": total_locations,
        "total_items": total_items,
        "recent_transactions": recent_transactions,
    }

    return render(request, "inventory/dashboard.html", context)
