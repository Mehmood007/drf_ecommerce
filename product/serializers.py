from rest_framework import serializers

from .models import Brand, Category, Product, ProductLine


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ProductLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLine
        exclude = ('id', 'product', 'is_active', 'created_at', 'updated_at')


class ProductSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name')
    category_name = serializers.CharField(source='category.name')
    product_line = ProductLineSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'name',
            'slug',
            'brand_name',
            'category_name',
            'description',
            'product_line',
        )
