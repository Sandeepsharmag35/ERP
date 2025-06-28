from rest_framework import serializers
from .models import Warehouse, InventoryLocation, InventoryItem, InventoryTransaction
from product.models import Product
from product.serializers import ProductSerializer


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = "__all__"


class InventoryLocationSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)
    warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(), source="warehouse", write_only=True
    )

    class Meta:
        model = InventoryLocation
        fields = [
            "location_id",
            "code",
            "name",
            "location_type",
            "is_active",
            "warehouse",
            "warehouse_id",
        ]


class InventoryItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    def validate(self, data):
        if data["quantity_on_hand"] < 0:
            raise serializers.ValidationError("Quantity on hand cannot be negative.")
        if data["unit_cost"] < 0 or data["total_cost"] < 0:
            raise serializers.ValidationError("Cost values cannot be negative.")
        return data

    class Meta:
        model = InventoryItem
        fields = [
            "inventory_item_id",
            "organization_id",
            "product",
            "product_id",
            "warehouse",
            "location",
            "quantity_on_hand",
            "unit_cost",
            "total_cost",
        ]
        depth = 1  # show nested warehouse/location/product


class InventoryTransactionSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data["quantity"] <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        if data["unit_cost"] < 0:
            raise serializers.ValidationError("Unit cost cannot be negative.")

        return data

    def create(self, validated_data):
        # Auto-compute total cost (business logic)
        validated_data["total_cost"] = (
            validated_data["quantity"] * validated_data["unit_cost"]
        )
        return super().create(validated_data)

    class Meta:
        model = InventoryTransaction
        fields = "__all__"
        depth = 1
