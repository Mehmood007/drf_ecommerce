from rest_framework import serializers

from .models import Brand, Category, Product, ProductImage, ProductLine


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ('id', 'product_line')


class ProductLineSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = (
            'price',
            'sku',
            'stock_qty',
            'order',
            'product_image',
        )


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
