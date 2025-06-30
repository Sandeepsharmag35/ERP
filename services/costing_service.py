from django.db import transaction
from inventory.models import InventoryItem


class CostingService:
    @staticmethod
    def cost_engine(transaction):
        """
        Apply FIFO/AVG costing methods and update moving-average cost on receipt
        """
        product = transaction.product
        inventory_item = InventoryItem.objects.get(
            product=product, warehouse_id=transaction.to_warehouse_id
        )

        if product.costing_method == "AVG":
            # Calculate new average cost
            old_total = inventory_item.quantity_on_hand * inventory_item.unit_cost
            new_total = transaction.quantity * transaction.unit_cost
            new_quantity = inventory_item.quantity_on_hand + transaction.quantity

            if new_quantity > 0:
                new_average_cost = (old_total + new_total) / new_quantity
                inventory_item.unit_cost = new_average_cost
                inventory_item.total_cost = new_quantity * new_average_cost
                inventory_item.save()

        elif product.costing_method == "FIFO":
            # For FIFO, we maintain the original transaction cost
            # This will be used when goods are sold/consumed
            pass  # Detailed FIFO implementation will be in Phase 2

        # Standard cost doesn't change based on receipt cost
        return inventory_item
