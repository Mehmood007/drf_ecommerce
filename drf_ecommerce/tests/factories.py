import factory
from factory.faker import faker

from product.models import Brand, Category, Product

Fake = faker.Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.sequence(lambda n: 'Categpry_%d' % n)


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = name = factory.sequence(lambda n: 'Brand_%d' % n)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = Fake.word()
    description = Fake.paragraph()
    is_digital = Fake.boolean()
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)
