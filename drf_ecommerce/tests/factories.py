import factory
from factory.faker import faker

from product.models import (
    Attribute,
    AttributeValue,
    Brand,
    Category,
    Product,
    ProductImage,
    ProductLine,
    ProductType,
)

fake = faker.Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.sequence(lambda n: 'Categpry_%d' % n)


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.sequence(lambda n: 'Brand_%d' % n)


class AttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attribute

    name = fake.word()
    description = fake.paragraph()


class AttributeValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AttributeValue

    attribute_value = fake.word()
    attribute = factory.SubFactory(AttributeFactory)


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType

    name = fake.word()

    @factory.post_generation
    def attribute(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.attribute.add(*extracted)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = fake.word()
    description = fake.paragraph()
    is_digital = fake.boolean()
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)
    product_type = factory.SubFactory(ProductTypeFactory)
    is_active = True


class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine

    price = fake.random_number(digits=2)
    sku = fake.bothify(text='????-###')
    stock_qty = fake.random_number(digits=1)
    product = factory.SubFactory(ProductFactory)
    is_active = True


class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage

    alternative_text = fake.sentence()
    url = 'test.jpg'
    product_line = factory.SubFactory(ProductLineFactory)
