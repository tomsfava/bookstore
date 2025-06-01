import pytest

from product.serializers import ProductSerializer
from product.tests import ProductFactory

@pytest.mark.django_db
def test_product_serializer_output():
    product = ProductFactory()
    serializer = ProductSerializer(product)

    data = serializer.data

    assert data["id"] == product.id
    assert data["title"] == product.title
    assert data["description"] == product.description
    assert float(data["price"]) == float(product.price)
    assert data["active"] == product.active

    category_titles = [cat.title for cat in product.category.all()]
    serialized_titles = [cat["title"] for cat in data["category"]]

    assert set(category_titles) == set(serialized_titles)
