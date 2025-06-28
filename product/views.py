from rest_framework import viewsets
from .models import Product, ProductUom, Uom
from .serializers import ProductSerializer, ProductUomSerializer, UomSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UomViewSet(viewsets.ModelViewSet):
    queryset = Uom.objects.all()
    serializer_class = UomSerializer


class ProductUomViewSet(viewsets.ModelViewSet):
    queryset = ProductUom.objects.all()
    serializer_class = ProductUomSerializer
