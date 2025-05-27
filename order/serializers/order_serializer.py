from rest_framework import serializers

from order.models import Order
from product.models import Product
from product.serializers import ProductSerializer

class OrderSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all(), write_only=True)
    products = ProductSerializer(source="product", many=True, read_only=True)
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        total = sum([p.price for p in instance.product.all()])
        return total

    class Meta:
        model = Order
        fields = ['user', 'products', 'product', 'total']

    def create(self, validated_data):
        products = validated_data.pop('product')
        order = Order.objects.create(**validated_data)
        order.product.set(products)
        return order