from django.db import models
from erp.models import UserOrganizationMixin, TimestampedModel
import uuid


class Uom(UserOrganizationMixin, TimestampedModel, models.Model):
    code = models.CharField(max_length=20, unique=True)  # e.g., 'EA', 'KG'
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=80)  # e.g., 'weight', 'length', 'qty'
    conversion_to_si = models.DecimalField(max_digits=15, decimal_places=4)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Product(UserOrganizationMixin, TimestampedModel, models.Model):
    class CostingMethod(models.TextChoices):
        FIFO = "FIFO", "FIFO"
        AVG = "AVG", "Average"
        STD = "STD", "Standard"

    class TrackingMethod(models.TextChoices):
        NONE = "NONE", "None"
        SERIAL = "SERIAL", "Serial"
        BATCH = "BATCH", "Batch"

    product_code = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    base_uom = models.ForeignKey("product.Uom", on_delete=models.PROTECT)
    costing_method = models.CharField(max_length=15, choices=CostingMethod.choices)
    tracking_method = models.CharField(max_length=15, choices=TrackingMethod.choices)
    safety_stock = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    reorder_qty = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cogs_account_id = models.UUIDField(default=uuid.uuid4)
    inventory_account_id = models.UUIDField(default=uuid.uuid4)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("organization", "product_code")

    def __str__(self):
        return self.name


class ProductUom(UserOrganizationMixin, TimestampedModel, models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    uom = models.ForeignKey(Uom, on_delete=models.CASCADE)
    factor = models.DecimalField(max_digits=15, decimal_places=4)
    is_default_sales = models.BooleanField(default=False)
    is_default_purchase = models.BooleanField(default=False)

    class Meta:
        unique_together = ("product", "uom")

    def __str__(self):
        return f"{self.product.name} - {self.uom.code}"
