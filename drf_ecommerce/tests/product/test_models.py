import pytest
from django.core.exceptions import ValidationError

pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_method(self, category_factory):
        category = category_factory()
        assert category.__str__() == category.name


class TestBrandModel:
    def test_str_method(self, brand_factory):
        brand = brand_factory()
        assert brand.__str__() == brand.name


class TestProductModel:
    def test_str_method(self, product_factory):
        product = product_factory()
        assert product.__str__() == product.name


class TestProductLineModel:
    def test_str_method(self, product_line_factory):
        product_line = product_line_factory()
        assert product_line.__str__() == product_line.sku

    def test_duplicate_order_values(self, product_line_factory, product_factory):
        product = product_factory()
        product_line = product_line_factory(order=1, product=product)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=product)


class TestProductTypeModel:
    def test_str_method(self, product_type_factory, attribute_factory):
        product_type = product_type_factory.create(attribute=(attribute_factory(),))
        assert product_type.__str__() == product_type.name


class TestProductImageModel:
    def test_str_method(self, product_image_factory):
        product_image = product_image_factory()
        assert product_image.__str__() == product_image.url


class TestAttributeModel:
    def test_str_method(self, attribute_factory):
        attribute = attribute_factory()
        assert attribute.__str__() == attribute.name


class TestAttributeValueModel:
    def test_str_method(self, attribute_value_factory):
        attribute_value = attribute_value_factory()
        assert (
            attribute_value.__str__()
            == f'{attribute_value.attribute} {attribute_value.attribute_value}'
        )
