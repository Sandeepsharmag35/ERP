from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Product, UoM, ProductUoM
from .serializers import ProductSerializer, UoMSerializer, ProductUoMSerializer


class UoMViewSet(viewsets.ModelViewSet):
    queryset = UoM.objects.all()
    serializer_class = UoMSerializer

    @extend_schema(description="List all Units of Measure")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(organization_id=self.request.user.organization_id)

    @action(detail=True, methods=["post"])
    def add_alternate_uom(self, request, pk=None):
        product = self.get_object()
        serializer = ProductUoMSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
