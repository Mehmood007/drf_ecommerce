from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Brand, Category, Product, ProductImage, ProductLine


class EditLinkInline:
    def edit(self, instance):
        url = reverse(
            f'admin:{instance._meta.app_label}_{instance._meta.model_name}_change',
            args=[instance.pk],
        )
        if instance.pk:
            link = mark_safe('<a href="{u}">edit</a>'.format(u=url))
            return link


class ProductLineInLine(EditLinkInline, admin.TabularInline):
    model = ProductLine
    readonly_fields = ('edit',)


class ProductImageInLine(admin.TabularInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductLineInLine]


class ProductLineAdmin(admin.ModelAdmin):
    inlines = [ProductImageInLine]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductLine, ProductLineAdmin)
