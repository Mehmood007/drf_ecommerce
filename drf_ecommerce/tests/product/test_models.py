import pytest

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
