import json

import pytest

pytestmark = pytest.mark.django_db


class TestCategoryEndpoint:
    endpoint = '/api/category/'

    def test_category_get(self, category_factory, api_client):
        category_factory.create_batch(4)
        response = api_client().get(self.endpoint)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4


class TestProductEndpoint:
    endpoint = '/api/products/'

    def test_return_all_products(self, product_factory, api_client):
        product_factory.create_batch(4)
        response = api_client().get(self.endpoint)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4

    def test_return_single_product_by_slug(self, product_factory, api_client):
        product = product_factory(slug='test-slug')
        response = api_client().get(f'{self.endpoint}{product.slug}/')
        assert response.status_code == 200
        assert json.loads(response.content)['slug'] == product.slug

    def test_return_products_by_category_slug(
        self, category_factory, product_factory, api_client
    ):
        category = category_factory()
        product_factory(category=category)
        response = api_client().get(f'{self.endpoint}category/{category.slug}/')
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1
