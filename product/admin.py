from django.contrib import admin
from .models import Uom, Product, ProductUom

admin.site.register(Uom)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "product_code",
        "base_uom",
        "is_active",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "product_code")
    list_filter = ("is_active", "organization")


@admin.register(ProductUom)
class ProductUomAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "uom", "factor")
    search_fields = ("product__name", "uom__name")
    list_filter = ("product__organization",)
