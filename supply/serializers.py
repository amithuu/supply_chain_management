from rest_framework import serializers
from .models import *


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'name', 'contact_info']


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id','product', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    shipment = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'order_date', 'status', 'order_items', 'shipment']

    def get_shipment(self, obj):
        shipment = Shipment.objects.filter(order=obj).first()
        if shipment:
            return {
                "id": shipment.id,
                "shipment_date": shipment.shipment_date,
                "delivery_date": shipment.delivery_date,
                "status": shipment.status
            }
        return None

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for item_data in order_items_data:
            product = Product.objects.get(pk=item_data['product'].id)
            OrderItem.objects.create(order=order, **item_data)

            # Update product stock
            product.stock -= item_data['quantity']
            product.save()

        # Create a shipment for the order
        Shipment.objects.create(order=order, shipment_date=order.order_date, status='Shipped')

        return order

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('order_items', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if order_items_data:
            # Clear existing items
            instance.order_items.all().delete()
            for item_data in order_items_data:
                product = Product.objects.get(pk=item_data['product'].id)
                OrderItem.objects.create(order=instance, **item_data)

                # Update product stock
                product.stock -= item_data['quantity']
                product.save()

        # Update the shipment for the order
        shipment = instance.shipment
        shipment.status = 'Shipped'
        shipment.save()

        return instance