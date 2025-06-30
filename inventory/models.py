from django.db import models
from usermanagement.models import UserOrganizationMixin, TimestampedModel
from product.models import Product


class TransactionType(models.TextChoices):
    IN = "IN", "Stock In"
    OUT = "OUT", "Stock Out"
    XFER = "XFER", "Transfer"
    ADJ = "ADJ", "Adjustment"


class Warehouse(UserOrganizationMixin, TimestampedModel):
    warehouse_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    address = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ["organization", "code"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class InventoryLocation(UserOrganizationMixin, TimestampedModel):
    location_id = models.AutoField(primary_key=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    location_type = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("warehouse", "code")


class InventoryItem(UserOrganizationMixin, TimestampedModel):
    inventory_item_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    location = models.ForeignKey(InventoryLocation, on_delete=models.PROTECT)
    quantity_on_hand = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} @ {self.location.code}: {self.quantity_on_hand}"


class InventoryTransaction(UserOrganizationMixin, TimestampedModel):
    transaction_id = models.AutoField(primary_key=True)
    transaction_type = models.CharField(max_length=4, choices=TransactionType.choices)
    transaction_date = models.DateTimeField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    from_warehouse = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT, related_name="from_transactions", null=True
    )
    to_warehouse = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT, related_name="to_transactions", null=True
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    journal_id = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.product.name} - {self.quantity}"
