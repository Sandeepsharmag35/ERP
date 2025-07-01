from django.db import transaction
from inventory.models import (
    InventoryItem,
    InventoryTransaction,
    Warehouse,
    InventoryLocation,
)
from product.models import Product
from services.costing_service import CostingService


class InventoryService:
    @staticmethod
    @transaction.atomic
    def post_stock_movement(user, dto):
        """
        Handles both UI form submissions and DRF API calls.
        DTO can contain either model instances or UUIDs for related fields.
        """
        # Validate organization access
        # if not user.has_organization_access(dto["organization_id"]):
        #     raise PermissionError("No access to this organization")

        def get_instance(model, value, field_name):
            if isinstance(value, model):
                return value
            if value:
                return model.objects.get(pk=value)
            return None

        # Resolve required objects
        product = get_instance(
            Product, dto.get("product") or dto.get("product_id"), "product"
        )
        from_warehouse = get_instance(
            Warehouse, dto.get("from_warehouse"), "from_warehouse"
        )
        to_warehouse = get_instance(Warehouse, dto.get("to_warehouse"), "to_warehouse")
        location = get_instance(
            InventoryLocation, dto.get("location") or dto.get("location_id"), "location"
        )

        # Validate product
        if product.tracking_method == "SERIAL":
            raise ValueError("Serial tracking not implemented in Phase 1")

        # Create the inventory transaction
        transaction_record = InventoryTransaction.objects.create(
            user=user,
            organization_id=dto.get("organization_id"),
            transaction_type=dto["transaction_type"],
            transaction_date=dto["transaction_date"],
            product=product,
            quantity=dto["quantity"],
            unit_cost=dto["unit_cost"],
            from_warehouse=from_warehouse,
            to_warehouse=to_warehouse,
            journal_id=dto.get("journal_id"),
        )

        # Determine effective warehouse
        effective_warehouse = (
            to_warehouse if dto["transaction_type"] == "IN" else from_warehouse
        )

        # Get or create InventoryItem
        inventory_item, _ = InventoryItem.objects.get_or_create(
            user=dto["user"],
            organization_id=dto.get("organization_id"),
            product=product,
            warehouse=effective_warehouse,
            location=location,
            defaults={"quantity_on_hand": 0, "unit_cost": 0, "total_cost": 0},
        )

        # Update quantity
        if dto["transaction_type"] == "IN":
            inventory_item.quantity_on_hand += dto["quantity"]
        else:
            if inventory_item.quantity_on_hand < dto["quantity"]:
                raise ValueError("Insufficient stock")
            inventory_item.quantity_on_hand -= dto["quantity"]

        inventory_item.save()

        # Update cost (only for IN)
        if dto["transaction_type"] == "IN":
            CostingService.cost_engine(transaction_record, inventory_item)

        inventory_item.save()

        return {
            "transaction_id": transaction_record.transaction_id,
            "cost_amount": float(
                transaction_record.unit_cost * transaction_record.quantity
            ),
        }
