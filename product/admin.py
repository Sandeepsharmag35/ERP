from django.contrib import admin
from .models import Uom, Product, ProductUom

admin.site.register(Uom)
admin.site.register(Product)
admin.site.register(ProductUom)
