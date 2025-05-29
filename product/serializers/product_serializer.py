from rest_framework import serializers

from product.models import Product, Category
from product.serializers.category_serializer import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=True)
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True, many=True, source="category"
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "price",
            "active",
            "category",
            "categories",
        ]

    def create(self, validated_data):
        category_data = validated_data.pop("category")

        product = Product.objects.create(**validated_data)
        product.category.set(category_data)

        return product
