from rest_framework import serializers
from .models import Uom, Product, ProductUom


class UomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uom
        fields = "__all__"


class ProductUomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUom
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    base_uom = UomSerializer(read_only=True)
    base_uom_id = serializers.PrimaryKeyRelatedField(
        queryset=Uom.objects.all(), source="base_uom", write_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "organization_id",
            "product_code",
            "name",
            "base_uom",
            "base_uom_id",
            "costing_method",
            "tracking_method",
            "safety_stock",
            "reorder_qty",
            "cogs_account_id",
            "inventory_account_id",
            "is_active",
        ]
