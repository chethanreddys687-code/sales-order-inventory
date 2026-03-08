from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'


class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id','dealer','order_number','status','total_amount','created_at','items']
        read_only_fields = ['order_number','total_amount']

    def create(self, validated_data):

        items_data = validated_data.pop('items')

        order = Order.objects.create(**validated_data)

        total = 0

        for item in items_data:

            product = item['product']
            qty = item['quantity']

            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=qty,
                unit_price=product.price,
                line_total=product.price * qty
            )

            total += order_item.line_total

        order.total_amount = total
        order.save()

        return order