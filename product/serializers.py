from rest_framework import serializers
from .models import Product, UoM, ProductUoM


class UoMSerializer(serializers.ModelSerializer):
    class Meta:
        model = UoM
        fields = ["uom_id", "code", "name", "category", "conversion_to_si"]

    def validate_code(self, value):
        if UoM.objects.filter(code=value).exists():
            raise serializers.ValidationError("UoM code must be unique")
        return value


class ProductUoMSerializer(serializers.ModelSerializer):
    uom_details = UoMSerializer(source="uom", read_only=True)

    class Meta:
        model = ProductUoM
        fields = [
            "uom_id",
            "factor",
            "is_default_sales",
            "is_default_purchase",
            "uom_details",
        ]


class ProductSerializer(serializers.ModelSerializer):
    base_uom = UoMSerializer(read_only=True)
    alternate_uoms = ProductUoMSerializer(
        source="productuom_set", many=True, read_only=True
    )

    class Meta:
        model = Product
        fields = [
            "product_id",
            "organization_id",
            "product_code",
            "name",
            "base_uom",
            "costing_method",
            "tracking_method",
            "safety_stock",
            "reorder_qty",
            "cogs_account_id",
            "inventory_account_id",
            "is_active",
            "alternate_uoms",
        ]

    def validate_product_code(self, value):
        if Product.objects.filter(
            organization_id=self.context["request"].user.organization_id,
            product_code=value,
        ).exists():
            raise serializers.ValidationError(
                "Product code must be unique within organization"
            )
        return value
