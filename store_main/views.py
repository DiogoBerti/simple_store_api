from rest_framework import viewsets, mixins, views
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Client, Product, SaleOrder, SaleOrderLine
from .serializers import ClientSerializer, ProductSerializer, SaleOrderSerializer, SaleOrderLineSerializer

class ClientViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
        ViewSet to manipulate and retrieve data from the Client model
    """

    queryset = Client.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ClientSerializer

class ProductViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
        ViewSet to manipulate and retrieve data from the Product model
    """

    queryset = Product.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

class SaleOrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
        ViewSet to manipulate and retrieve data from the SaleOrder model
    """

    queryset = SaleOrder.objects.all()
    permission_classes = [AllowAny]
    serializer_class = SaleOrderSerializer

class SaleOrderLineViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
        ViewSet to manipulate and retrieve data from the SaleOrderLine model
    """

    queryset = SaleOrderLine.objects.all()
    permission_classes = [AllowAny]
    serializer_class = SaleOrderLineSerializer