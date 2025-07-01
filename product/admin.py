from django.contrib import admin
from .models import UoM, Product, ProductUoM

admin.site.register(UoM)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "product_id",
        "name",
        "product_code",
        "base_uom",
        "is_active",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "product_code")
    list_filter = ("is_active", "organization")
    ordering = ("name",)


@admin.register(ProductUoM)
class ProductUoMAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "uom", "factor")
    search_fields = ("product__name", "uom__name")
    list_filter = ("product__organization",)
    name = "Product Unit of Measure"
    ordering = ("product__name", "uom__name")



admin.site.site_header = "ERP Product Management"
admin.site.site_title = "ERP Product Admin"
admin.site.index_title = "Product Management Dashboard"
