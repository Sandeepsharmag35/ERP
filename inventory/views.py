from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from services.inventory_service import InventoryService
from .models import Warehouse, InventoryLocation, InventoryItem, InventoryTransaction
from .serializers import (
    WarehouseSerializer, InventoryLocationSerializer,
    InventoryItemSerializer, StockMovementSerializer
)

class WarehouseViewSet(viewsets.ModelViewSet):
    serializer_class = WarehouseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Warehouse.objects.filter(
            organization_id=self.request.user.organization_id
        )

class InventoryLocationViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryLocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return InventoryLocation.objects.filter(
            warehouse__organization_id=self.request.user.organization_id
        )

class StockViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return InventoryItem.objects.filter(
            organization_id=self.request.user.organization_id
        )

    @action(detail=False, methods=['post'])
    def movement(self, request):
        try:
            result = InventoryService.post_stock_movement(
                user=request.user,
                dto=request.data
            )
            return Response(result)
        except ValueError as e:
            return Response({'error': str(e)}, status=400)