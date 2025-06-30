from django.db import models
from usermanagement.models import UserOrganizationMixin, TimestampedModel
import uuid


class CostingMethod(models.TextChoices):
    FIFO = "FIFO", "First In First Out"
    AVG = "AVG", "Average Cost"
    STD = "STD", "Standard Cost"


class TrackingMethod(models.TextChoices):
    NONE = "NONE", "No Tracking"
    SERIAL = "SERIAL", "Serial Number"
    BATCH = "BATCH", "Batch Number"


class UoM(UserOrganizationMixin, TimestampedModel):
    uom_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=20)
    conversion_to_si = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Product(UserOrganizationMixin, TimestampedModel):
    product_id = models.AutoField(primary_key=True)
    product_code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    base_uom = models.ForeignKey(UoM, on_delete=models.PROTECT)
    costing_method = models.CharField(
        max_length=4, choices=CostingMethod.choices, default=CostingMethod.AVG
    )
    tracking_method = models.CharField(
        max_length=6, choices=TrackingMethod.choices, default=TrackingMethod.NONE
    )
    safety_stock = models.DecimalField(max_digits=10, decimal_places=2)
    reorder_qty = models.DecimalField(max_digits=10, decimal_places=2)
    cogs_account_id = models.UUIDField(default=uuid.uuid4)
    inventory_account_id = models.UUIDField(default=uuid.uuid4)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ["organization", "product_code"]

    def __str__(self):
        return self.name


class ProductUoM(UserOrganizationMixin, TimestampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    uom = models.ForeignKey(UoM, on_delete=models.CASCADE)
    factor = models.DecimalField(max_digits=10, decimal_places=4)
    is_default_sales = models.BooleanField(default=False)
    is_default_purchase = models.BooleanField(default=False)

    class Meta:
        unique_together = ["product", "uom"]

    def __str__(self):
        return f"{self.product.name} - {self.uom.code}"
