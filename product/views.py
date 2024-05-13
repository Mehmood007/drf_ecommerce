from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Product, ProductImage, ProductLine
from .serializers import (
    CategorySerializer,
    ProductCategorySerializer,
    ProductSerializer,
)


class CategoryViewSet(viewsets.ViewSet):
    '''
    Simple view set for viewing categories
    '''

    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    '''
    Simple view set for viewing products
    '''

    queryset = Product.objects.all().isactive()
    lookup_field = 'slug'

    def retrieve(self, request, slug=None):
        serializer = ProductSerializer(
            self.queryset.select_related('category')
            .prefetch_related(Prefetch('product_line__product_image'))
            .prefetch_related(Prefetch('product_line__attribute_values__attribute'))
            .get(slug=slug)
        )
        return Response(serializer.data)

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path=r'category/(?P<slug>\w+)')
    def list_items_by_category_slug(self, request, slug=None):
        '''
        An endpoint to return products by category
        '''
        serializer = ProductCategorySerializer(
            self.queryset.filter(category__slug=slug)
            .prefetch_related(
                Prefetch('product_line', queryset=ProductLine.objects.order_by('order'))
            )
            .prefetch_related(
                Prefetch(
                    'product_line__product_image',
                    queryset=ProductImage.objects.filter(order=1),
                )
            ),
            many=True,
        )
        return Response(serializer.data)
