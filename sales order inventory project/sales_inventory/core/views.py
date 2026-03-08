from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

from .models import Product, Dealer, Order, Inventory
from .serializers import ProductSerializer, DealerSerializer, OrderSerializer, InventorySerializer


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()

    serializer_class = ProductSerializer

    def perform_create(self, serializer):

        product = serializer.save()

        Inventory.objects.create(product=product, quantity=0)


class DealerViewSet(viewsets.ModelViewSet):

    queryset = Dealer.objects.all()

    serializer_class = DealerSerializer


class OrderViewSet(viewsets.ModelViewSet):

    queryset = Order.objects.all()

    serializer_class = OrderSerializer


    def update(self, request, *args, **kwargs):

        order = self.get_object()

        if order.status != "draft":

            return Response({"error": "Only draft orders can be edited"}, status=400)

        return super().update(request, *args, **kwargs)


    @action(detail=True, methods=["post"])

    def confirm(self, request, pk=None):

        order = self.get_object()

        if order.status != "Draft":

            return Response({"error": "Only draft orders can be confirmed"}, status=400)

        with transaction.atomic():

            for item in order.items.all():

                stock = item.product.inventory.quantity

                if item.quantity > stock:

                    return Response({
                        "error": f"Insufficient stock for {item.product.name}. Available: {stock}, Requested: {item.quantity}"
                    })

            for item in order.items.all():

                inventory = item.product.inventory

                inventory.quantity -= item.quantity

                inventory.save()

            order.status = "Confirmed"

            order.save()

        return Response({"message": "Order confirmed"})


    @action(detail=True, methods=["post"])

    def deliver(self, request, pk=None):

        order = self.get_object()

        if order.status != "Confirmed":

            return Response({"error": "Only confirmed orders can be delivered"}, status=400)

        order.status = "Delivered"

        order.save()

        return Response({"message": "Order delivered"})


class InventoryViewSet(viewsets.ModelViewSet):

    queryset = Inventory.objects.all()

    serializer_class = InventorySerializer