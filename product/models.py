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
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self) -> str:
        return self.name


class Brand(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = TreeForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, blank=True
    )
    is_active = models.BooleanField(default=False)

    objects = ActiveQuerySet().as_manager()

    def __str__(self) -> str:
        return self.name


class ProductLine(BaseModel):
    price = models.DecimalField(decimal_places=2, max_digits=8)
    sku = models.CharField(max_length=100)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_line'
    )
    is_active = models.BooleanField(default=False)
    order = OrderField(unique_for_field='product', blank=True)

    objects = ActiveQuerySet().as_manager()

    def clean(self):
        qs = ProductLine.objects.filter(product=self.product)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError('Duplicate value detected')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLine, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.sku
