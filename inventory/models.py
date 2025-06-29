from django.db import models
from erp.models import UserOrganizationMixin, TimestampedModel
import uuid


class Warehouse(UserOrganizationMixin, TimestampedModel, models.Model):
    warehouse_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("organization", "code")

    def __str__(self):
        return f"{self.name} ({self.code})"


class InventoryLocation(UserOrganizationMixin, TimestampedModel, models.Model):
    location_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    location_type = models.CharField(max_length=80)  # e.g., aisle/bin
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("warehouse", "code")

    def __str__(self):
        return f"{self.name} ({self.code}) in {self.warehouse.code}"


class InventoryItem(UserOrganizationMixin, TimestampedModel, models.Model):
    inventory_item_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    product = models.ForeignKey("product.Product", on_delete=models.PROTECT)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    location = models.ForeignKey(InventoryLocation, on_delete=models.PROTECT)
    quantity_on_hand = models.DecimalField(max_digits=12, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=4)
    total_cost = models.DecimalField(max_digits=14, decimal_places=4)

    def __str__(self):
        return f"{self.product.name} @ {self.location.code}: {self.quantity_on_hand}"


class InventoryTransaction(UserOrganizationMixin, TimestampedModel, models.Model):
    class TransactionType(models.TextChoices):
        IN = "IN", "Inbound"
        OUT = "OUT", "Outbound"
        XFER = "XFER", "Transfer"
        ADJ = "ADJ", "Adjustment"

    transaction_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices)
    transaction_date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey("product.Product", on_delete=models.PROTECT)
    from_warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions_from",
    )
    to_warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions_to",
    )
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=4)
    journal_id = models.UUIDField(null=True, blank=True)  # stub for Phase-2

    def __str__(self):
        return f"{self.transaction_type} - {self.product.name} - {self.quantity}"
