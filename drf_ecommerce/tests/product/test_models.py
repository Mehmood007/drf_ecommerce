import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from product.models import Product, ProductLine

pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_method(self, category_factory):
        category = category_factory()
        assert category.__str__() == category.name

    def test_max_name_length(self, category_factory):
        name = 'x' * 101
        object = category_factory(name=name)
        with pytest.raises(ValidationError):
            object.full_clean()

    def test_max_slug_length(self, category_factory):
        slug = 'x' * 151
        object = category_factory(slug=slug)
        with pytest.raises(ValidationError):
            object.full_clean()

    def test_unique_name_field(self, category_factory):
        category_factory(name='test_name')
        with pytest.raises(IntegrityError):
            category_factory(name='test_name')

    def test_unique_slug_field(self, category_factory):
        category_factory(slug='test_slug')
        with pytest.raises(IntegrityError):
            category_factory(slug='test_slug')

    def test_category_on_delete_protect(self, category_factory):
        parent_category = category_factory()
        category_factory(parent=parent_category)
        with pytest.raises(IntegrityError):
            parent_category.delete()

    def test_parent_field_is_null(self, category_factory):
        category = category_factory()
        assert category.parent is None


class TestProductModel:
    def test_str_method(self, product_factory):
        product = product_factory()
        assert product.__str__() == product.name

    def test_max_name_length(self, product_factory):
        name = 'x' * 101
        object = product_factory(name=name)
        with pytest.raises(ValidationError):
            object.full_clean()

    def test_max_slug_length(self, product_factory):
        slug = 'x' * 256
        object = product_factory(slug=slug)
        with pytest.raises(ValidationError):
            object.full_clean()

    def test_max_pid_length(self, product_factory):
        pid = 'x' * 11
        object = product_factory(pid=pid)
        with pytest.raises(ValidationError):
            object.full_clean()

    def test_fk_category_on_delete_protect(self, category_factory, product_factory):
        category = category_factory()
        product_factory(category=category)
        with pytest.raises(IntegrityError):
            category.delete()

    def test_return_product_active_only_true(self, product_factory):
        product_factory(is_active=False)
        product_factory(is_active=True)
        qs = Product.objects.isactive().count()
        assert qs == 1

    def test_return_product_active_only_false(self, product_factory):
        product_factory(is_active=False)
        product_factory(is_active=True)
        qs = Product.objects.count()
        assert qs == 2


class TestProductLineModel:
    def test_str_method(self, product_line_factory):
        product_line = product_line_factory()
        assert product_line.__str__() == product_line.sku

    def test_duplicate_order_values(self, product_line_factory, product_factory):
        product = product_factory()
        product_line_factory(order=1, product=product)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=product)

    def test_price_decimal_places(self, product_line_factory):
        price = 1.001
        with pytest.raises(ValidationError):
            product_line_factory(price=price)

    def test_price_digits_places(self, product_line_factory):
        price = 1000000.00
        with pytest.raises(ValidationError):
            product_line_factory(price=price)

    def test_max_slug_length(self, product_line_factory):
        sku = 'x' * 101
        with pytest.raises(ValidationError):
            product_line_factory(sku=sku)

    def test_return_product_line_active_only_true(self, product_line_factory):
        product_line_factory(is_active=False)
        product_line_factory(is_active=True)
        qs = ProductLine.objects.isactive().count()
        assert qs == 1

    def test_return_product_line_active_only_false(self, product_line_factory):
        product_line_factory(is_active=False)
        product_line_factory(is_active=True)
        qs = ProductLine.objects.count()
        assert qs == 2

    def test_duplicate_value_insert(
        self,
        product_line_factory,
        attribute_factory,
        attribute_value_factory,
        product_line_attribute_value_factory,
    ):
        obj1 = attribute_factory(name='shoe-color')
        obj2 = attribute_value_factory(attribute_value='red', attribute=obj1)
        obj2 = attribute_value_factory(attribute_value='blue', attribute=obj1)
        obj4 = product_line_factory()
        product_line_attribute_value_factory(attribute_value=obj2, product_line=obj4)
        with pytest.raises(ValidationError):
            product_line_attribute_value_factory(
                attribute_value=obj2, product_line=obj4
            )


class TestProductTypeModel:
    def test_str_method(self, product_type_factory, attribute_factory):
        product_type = product_type_factory.create(attribute=(attribute_factory(),))
        assert product_type.__str__() == product_type.name

    def test_max_name_length(self, product_type_factory):
        name = 'x' * 101
        with pytest.raises(ValidationError):
            product_type_factory(name=name).full_clean()


class TestProductImageModel:
    def test_str_method(self, product_image_factory):
        product_image = product_image_factory()
        assert product_image.__str__() == product_image.url

    def test_max_alternative_text_length(self, product_image_factory):
        alternative_text = 'x' * 101
        with pytest.raises(ValidationError):
            product_image_factory(alternative_text=alternative_text)

    def test_duplicate_order_values(self, product_image_factory, product_line_factory):
        obj = product_line_factory()
        product_image_factory(order=1, product_line=obj)
        with pytest.raises(ValidationError):
            product_image_factory(order=1, product_line=obj)


class TestAttributeModel:
    def test_str_method(self, attribute_factory):
        attribute = attribute_factory()
        assert attribute.__str__() == attribute.name

    def test_max_name_length(self, attribute_factory):
        name = 'x' * 101
        with pytest.raises(ValidationError):
            attribute_factory(name=name).full_clean()


class TestAttributeValueModel:
    def test_str_method(self, attribute_value_factory):
        attribute_value = attribute_value_factory()
        assert (
            attribute_value.__str__()
            == f'{attribute_value.attribute} {attribute_value.attribute_value}'
        )

    def test_max_name_length(self, attribute_value_factory):
        attribute_value = 'x' * 101
        with pytest.raises(ValidationError):
            attribute_value_factory(attribute_value=attribute_value).full_clean()
