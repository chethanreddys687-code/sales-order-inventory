from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

from .models import *
from .serializers import *


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class DealerViewSet(viewsets.ModelViewSet):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer


class OrderViewSet(viewsets.ModelViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):

        order = self.get_object()

        if order.status != "Draft":
            return Response({"error": "Only draft orders can be confirmed"})

        with transaction.atomic():

            for item in order.items.all():

                inventory = Inventory.objects.get(product=item.product)

                if item.quantity > inventory.quantity:
                    return Response({
                        "error": f"Insufficient stock for {item.product.name}. Available {inventory.quantity}"
                    })

            for item in order.items.all():
                inventory = Inventory.objects.get(product=item.product)
                inventory.quantity -= item.quantity
                inventory.save()

        order.status = "Confirmed"
        order.save()

        return Response({"message": "Order confirmed"})


    @action(detail=True, methods=['post'])
    def deliver(self, request, pk=None):

        order = self.get_object()

        if order.status != "Confirmed":
            return Response({"error": "Order must be confirmed first"})

        order.status = "Delivered"
        order.save()

        return Response({"message": "Order delivered"})