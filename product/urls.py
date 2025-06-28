from django.urls import path
from . import ui_views

urlpatterns = [
    path("products/", ui_views.product_list, name="product-list"),
    path("products/create/", ui_views.product_create, name="product-create"),
    path("products/<int:pk>/", ui_views.product_detail, name="product-detail"),
    path("uoms/", ui_views.uom_list, name="uom-list"),
    path("uoms/create/", ui_views.uom_create, name="uom-create"),
    path(
        "products/<int:product_pk>/uoms/create/",
        ui_views.product_uom_create,
        name="product-uom-create",
    ),
]
