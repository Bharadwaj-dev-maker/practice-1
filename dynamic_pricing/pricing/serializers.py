from rest_framework import serializers
from .models import Product, Discount, Order, OrderProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, write_only=True)
    discounts = serializers.PrimaryKeyRelatedField(queryset=Discount.objects.all(), many=True)
    total_price = serializers.FloatField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'products', 'discounts', 'total_price']

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        discounts = validated_data.pop('discounts')
        order = Order.objects.create(**validated_data)
        for product_data in products_data:
            OrderProduct.objects.create(order=order, **product_data)
        order.discounts.set(discounts)
        order.calculate_total()
        return order
