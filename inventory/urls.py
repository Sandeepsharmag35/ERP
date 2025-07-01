from django.urls import path
from . import ui_views

urlpatterns = [
    path("", ui_views.dashboard, name="dashboard"),
    # Warehouses
    path("warehouses/", ui_views.warehouse_list, name="warehouse_list"),
    path("warehouses/create/", ui_views.warehouse_create, name="warehouse_create"),
    path(
        "warehouses/<int:warehouse_id>/",
        ui_views.warehouse_detail,
        name="warehouse_detail",
    ),
    # Inventory Locations
    path(
        "warehouses/<int:warehouse_id>/locations/create/",
        ui_views.location_create,
        name="location_create",
    ),
    # Stock Management
    path("stock/", ui_views.stock_grid, name="stock_grid"),
    path(
        "stock-movements/", ui_views.stock_movement_create, name="stock_movement_create"
    ),
    # HTMX Partials
    path(
        "transaction-fields/",
        ui_views.transaction_fields_partial,
        name="transaction_fields_partial",
    ),
]
