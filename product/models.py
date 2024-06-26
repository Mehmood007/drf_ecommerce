from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey

from utils.base_model import BaseModel

from .fields import OrderField


class ActiveQuerySet(models.QuerySet):
    def isactive(self) -> models.QuerySet:
        return self.filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self) -> str:
        return self.name


class Product(BaseModel):
    pid = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    category = TreeForeignKey(
        'Category', on_delete=models.PROTECT, null=True, blank=True
    )
    attribute_values = models.ManyToManyField(
        'AttributeValue',
        through="ProductAttributeValue",
        related_name='product_attr_value',
    )
    product_type = models.ForeignKey("ProductType", on_delete=models.PROTECT)
    is_active = models.BooleanField(default=False)

    objects = ActiveQuerySet().as_manager()

    def __str__(self) -> str:
        return self.name


class Attribute(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class AttributeValue(BaseModel):
    attribute_value = models.CharField(max_length=100)
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name='attribute_value'
    )

    def __str__(self) -> str:
        return f'{self.attribute} {self.attribute_value}'


class ProductLine(BaseModel):
    price = models.DecimalField(decimal_places=2, max_digits=8)
    sku = models.CharField(max_length=100)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='product_line'
    )
    attribute_values = models.ManyToManyField(
        AttributeValue,
        through="ProductLineAttributeValue",
        related_name='product_line_attribute_value',
    )
    weight = models.FloatField()
    is_active = models.BooleanField(default=False)
    order = OrderField(unique_for_field='product', blank=True)

    objects = ActiveQuerySet().as_manager()

    def clean(self):
        try:
            qs = ProductLine.objects.filter(product=self.product)
        except:
            return
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError('Duplicate value detected')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLine, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.sku


class ProductLineAttributeValue(BaseModel):
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name='product_attribute_value_av',
    )
    product_line = models.ForeignKey(
        ProductLine, on_delete=models.CASCADE, related_name='product_attribute_value_pl'
    )

    class Meta:
        unique_together = ('attribute_value', 'product_line')

    def clean(self):
        qs = (
            ProductLineAttributeValue.objects.filter(
                attribute_value=self.attribute_value
            )
            .filter(product_line=self.product_line)
            .exists()
        )
        if not qs:
            iqs = Attribute.objects.filter(
                attribute_value__product_line_attribute_value=self.product_line
            ).values_list('pk', flat=True)

            if self.attribute_value.attribute.id in list(iqs):
                raise ValidationError('Duplicate attribute exists')

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        return super(ProductLineAttributeValue, self).save(*args, **kwargs)


class ProductImage(BaseModel):
    alternative_text = models.CharField(max_length=100)
    url = models.ImageField(upload_to='products', default='test.jpg')
    product_line = models.ForeignKey(
        ProductLine, on_delete=models.CASCADE, related_name='product_image'
    )
    order = OrderField(unique_for_field='product_line', blank=True)

    def clean(self):
        qs = ProductImage.objects.filter(product_line=self.product_line)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError('Duplicate value detected')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductImage, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.url}'


class ProductType(BaseModel):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
    attribute = models.ManyToManyField(
        Attribute, through='ProductTypeAttribute', related_name='product_type_attribute'
    )

    def __str__(self) -> str:
        return self.name


class ProductTypeAttribute(BaseModel):
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name='product_type_attribute_pt',
    )
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name='product_type_attribute_a'
    )

    class Meta:
        unique_together = ('product_type', 'attribute')


class ProductAttributeValue(BaseModel):
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name='product_value_av',
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_value_pl'
    )

    class Meta:
        unique_together = ('attribute_value', 'product')
