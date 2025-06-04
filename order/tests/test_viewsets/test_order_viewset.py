import json

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from django.urls import reverse

from product.factories import CategoryFactory, ProductFactory
from order.factories import UserFactory, OrderFactory
from order.models import Order


class TestOrderViewSet(APITestCase):

    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title="technology")
        self.product = ProductFactory(
            title="mouse", price=100.00, category=[self.category]
        )
        self.order = OrderFactory(product=[self.product])
        self.user = UserFactory()
        token = Token.objects.create(user=self.user)
        token.save()

    def test_order(self):
        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(reverse("order-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = json.loads(response.content)["results"][0]
        self.assertEqual(order_data["product"][0]["title"], self.product.title)
        self.assertEqual(
            float(order_data["product"][0]["price"]), float(self.product.price)
        )
        self.assertEqual(order_data["product"][0]["active"], self.product.active)
        self.assertEqual(
            order_data["product"][0]["category"][0]["title"], self.category.title
        )

    def test_create_order(self):
        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        product = ProductFactory()
        data = json.dumps({"products": [product.id], "user": self.user.id})

        response = self.client.post(
            reverse("order-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_order = Order.objects.get(user=self.user)
        self.assertIsNotNone(created_order)
        self.assertEqual(created_order.user.id, self.user.id)
        self.assertIn(product, created_order.product.all())
