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
