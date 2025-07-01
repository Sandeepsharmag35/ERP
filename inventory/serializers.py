from rest_framework import serializers
from .models import Warehouse, InventoryLocation, InventoryItem, InventoryTransaction


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = [
            "warehouse_id",
            "user",
            "organization_id",
            "code",
            "name",
            "address",
            "is_active",
        ]

    def validate_code(self, value):
        if Warehouse.objects.filter(
            organization_id=self.context["request"].user.organization_id, code=value
        ).exists():
            raise serializers.ValidationError(
                "Warehouse code must be unique within organization"
            )
        return value


class InventoryLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryLocation
        fields = [
            "location_id",
            "warehouse",
            "code",
            "name",
            "location_type",
            "is_active",
            "user",
            "organization_id",
        ]


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = [
            "inventory_item_id",
            "organization_id",
            "product",
            "warehouse",
            "location",
            "quantity_on_hand",
            "unit_cost",
            "total_cost",
        ]
        read_only_fields = ["quantity_on_hand", "unit_cost", "total_cost"]


class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryTransaction
        fields = [
            "transaction_id",
            "user",
            "organization_id",
            "transaction_type",
            "transaction_date",
            "product",
            "from_warehouse",
            "to_warehouse",
            "quantity",
            "unit_cost",
            "journal_id",
        ]
