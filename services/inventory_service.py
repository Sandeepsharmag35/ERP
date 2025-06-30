# services/inventory_service.py
from django.db import transaction
from decimal import Decimal
from inventory.models import InventoryItem, InventoryTransaction
from product.models import Product, ProductUoM, UoM


class InventoryService:
    @staticmethod
    @transaction.atomic
    def post_stock_movement(user, dto):
        # Validate organization access
        if not user.has_organization_access(dto["organization_id"]):
            raise PermissionError("No access to this organization")

        # Validate product and stock
        product = Product.objects.get(
            organization_id=dto["organization_id"], product_id=dto["product_id"]
        )

        # Check if serial tracking is required
        if product.tracking_method == "SERIAL":
            raise ValueError("Serial tracking not implemented in Phase 1")

        # Create transaction
        transaction = InventoryTransaction.objects.create(
            organization_id=dto["organization_id"],
            transaction_type=dto["transaction_type"],
            product=product,
            quantity=dto["quantity"],
            unit_cost=dto["unit_cost"],
            from_warehouse_id=dto.get("from_warehouse_id"),
            to_warehouse_id=dto.get("to_warehouse_id"),
            transaction_date=dto["transaction_date"],
        )

        # Update inventory items
        inventory_item, created = InventoryItem.objects.get_or_create(
            organization_id=dto["organization_id"],
            product=product,
            warehouse_id=(
                dto["to_warehouse_id"]
                if dto["transaction_type"] == "IN"
                else dto["from_warehouse_id"]
            ),
            location_id=dto["location_id"],
            defaults={"quantity_on_hand": 0, "unit_cost": 0, "total_cost": 0},
        )

        if dto["transaction_type"] == "IN":
            inventory_item.quantity_on_hand += dto["quantity"]
        else:
            if inventory_item.quantity_on_hand < dto["quantity"]:
                raise ValueError("Insufficient stock")
            inventory_item.quantity_on_hand -= dto["quantity"]

        # Update costs using costing engine
        if dto["transaction_type"] == "IN":
            CostingService.cost_engine(transaction)

        inventory_item.save()

        return {
            "transaction_id": transaction.transaction_id,
            "cost_amount": transaction.unit_cost * transaction.quantity,
        }

class UnitConversionService:
    @staticmethod
    def convert_qty(value: Decimal, from_uom: UoM, to_uom: UoM) -> Decimal:
        """
        Convert quantity between different units of measure using SI units as intermediate

        Args:
            value: The quantity to convert
            from_uom: Source UoM object
            to_uom: Target UoM object

        Returns:
            Converted quantity in target UoM

        Example:
            convert_qty(1, box_uom, ea_uom) -> 10  # if 1 box = 10 each
        """
        if from_uom == to_uom:
            return value

        # First convert to SI units
        si_value = value * from_uom.conversion_to_si

        # Then convert from SI to target UoM
        result = si_value / to_uom.conversion_to_si

        # If converting between UoMs for same product, use direct factor
        try:
            product_uom = ProductUoM.objects.get(product__base_uom=from_uom, uom=to_uom)
            result = value * product_uom.factor
        except ProductUoM.DoesNotExist:
            pass

        return result
