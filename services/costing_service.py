from inventory.models import InventoryItem


class CostingService:
    @staticmethod
    def cost_engine(transaction, inventory_item=None):
        """
        Apply costing method to the inventory item.
        Supports AVG and placeholder for FIFO.
        - If inventory_item is passed, it skips re-fetching.
        """

        product = transaction.product

        # Get inventory item if not already passed
        if not inventory_item:
            try:
                inventory_item = InventoryItem.objects.get(
                    product=product, warehouse_id=transaction.to_warehouse_id
                )
            except InventoryItem.DoesNotExist:
                raise ValueError("Inventory item not found for costing")

        # --- AVG Costing ---
        if product.costing_method == "AVG":
            old_qty = inventory_item.quantity_on_hand - transaction.quantity
            old_total = old_qty * inventory_item.unit_cost
            new_total = transaction.quantity * transaction.unit_cost
            new_quantity = inventory_item.quantity_on_hand

            if new_quantity > 0:
                new_average_cost = (old_total + new_total) / new_quantity
                inventory_item.unit_cost = new_average_cost
                inventory_item.total_cost = new_quantity * new_average_cost
                inventory_item.save()

        # --- FIFO Costing (To be implemented later) ---
        elif product.costing_method == "FIFO":
            pass  # Placeholder for FIFO logic in Phase 2

        # --- STD Costing (No cost update needed) ---
        # For STD (standard costing), cost is assumed fixed

        return inventory_item
