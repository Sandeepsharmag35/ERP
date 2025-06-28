from django.contrib import admin
from .models import Warehouse, InventoryLocation, InventoryItem, InventoryTransaction

admin.site.register(Warehouse)
admin.site.register(InventoryLocation)
admin.site.register(InventoryItem)
admin.site.register(InventoryTransaction)
