from rest_framework import serializers

from order.models import Order
from product.models import Product
from product.serializers import ProductSerializer

class OrderSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all(), write_only=True, source='product')
    product = ProductSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        total = sum([p.price for p in instance.product.all()])
        return total

    class Meta:
        model = Order
        fields = ['user', 'products', 'product', 'total']

    def create(self, validated_data):
        product_data = validated_data.pop('product')
        user = validated_data.pop('user')
        order = Order.objects.create(user=user)
        order.product.set(product_data)
        return order