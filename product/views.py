from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Brand, Category, Product
from .serializers import BrandSerializer, CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ViewSet):
    '''
    Simple view set for viewing categories
    '''

    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class BrandViewSet(viewsets.ViewSet):
    '''
    Simple view set for viewing brands
    '''

    queryset = Brand.objects.all()

    @extend_schema(responses=BrandSerializer)
    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    '''
    Simple view set for viewing products
    '''

    queryset = Product.objects.all().isactive()
    lookup_field = 'slug'

    def retrieve(self, request, slug=None):
        serializer = ProductSerializer(
            self.queryset.select_related('category', 'brand').get(slug=slug)
        )
        serializer.data
        return Response(serializer.data)

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path=r'category/(?P<category>\w+)')
    def list_items_by_category(self, request, category=None):
        '''
        An endpoint to return products by category
        '''
        serializer = ProductSerializer(
            self.queryset.filter(category__name=category), many=True
        )
        return Response(serializer.data)
