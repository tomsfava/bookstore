import factory

from product.models import Product
from product.models import Category

class CategoryFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('word')
    slug = factory.Faker('slug')
    description = factory.Faker('sentence')
    active = factory.Iterator([True, False])

    class Meta:
        model = Category

class ProductFactory(factory.django.DjangoModelFactory):
    price = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    title = factory.Faker('word')
    description = factory.Faker('sentence')
    active = factory.Iterator([True, False])

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for cat in extracted:
                self.category.add(cat)

        else:
            self.category.add(CategoryFactory())

    class Meta:
        model = Product