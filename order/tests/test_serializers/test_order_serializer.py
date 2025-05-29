import pytest

from order.serializers import OrderSerializer
from order.tests import UserFactory
from product.tests import ProductFactory

@pytest.mark.django_db
def test_order_serializer_valid_data():
    user = UserFactory()
    product1 = ProductFactory(price=30.00)
    product2 = ProductFactory(price=20.00)

    data = {
        "user": user.id,
        "product_id": [product1.id, product2.id],
    }

    serializer = OrderSerializer(data=data)
    assert serializer.is_valid(), serializer.errors

    order = serializer.save()

    assert order.user == user
    assert set(order.product.all()) == {product1, product2}

    assert serializer.data["total"] == 50.00

    returned_product_ids = {p["id"] for p in serializer.data["product"]}
    assert returned_product_ids == {product1.id, product2.id}