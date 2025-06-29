"""
URL configuration for erp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from product.views import ProductViewSet, ProductUomViewSet, UomViewSet
from inventory.views import (
    WarehouseViewSet,
    InventoryLocationViewSet,
    InventoryItemViewSet,
    InventoryTransactionViewSet,
)

router = DefaultRouter()
# Product
router.register(r"products", ProductViewSet)
router.register(r"uom", UomViewSet)
router.register(r"product-uom", ProductUomViewSet)

# Inventory
router.register(r"warehouses", WarehouseViewSet)
router.register(r"locations", InventoryLocationViewSet)
router.register(r"stock-items", InventoryItemViewSet)
router.register(r"stock-movements", InventoryTransactionViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("", include("product.urls")),
    path("", include("inventory.urls")),
]
