from django.contrib import admin
from .models import (
    Order,
    Product,
    ProductRemains,
    ProductVariant,
    ProductImage,
    OrderProduct,
    Category,
)
from django.utils.translation import gettext_lazy as _
from django import forms


class ProductAdminForm(forms.ModelForm):

    def clean(self):

        categories = self.cleaned_data.get('categories')
        if (categories is not None) and categories.filter(
            parent_prefix=_('Brands')
        ).count() > 1:

            self.add_error(
                'categories',
                _('Only one category with parent prefix "Brands" is allowed.')
            )

        return self.cleaned_data

    class Meta:
        model = Product
        exclude = []


class OrderPositionsInline(admin.TabularInline):
    model = OrderProduct


class ProductVariantInline(admin.TabularInline):
    model = ProductRemains


class ProductImageInline(admin.StackedInline):
    model = ProductImage


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderPositionsInline,
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    inlines = [
        ProductVariantInline,
        ProductImageInline,
    ]
    autocomplete_fields = ('categories',)


@admin.register(ProductRemains)
class ProductRemainsAdmin(admin.ModelAdmin):
    inlines = [
        OrderPositionsInline,
    ]


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    inlines = [
        ProductVariantInline,
    ]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_prefix')
    search_fields = ('name',)
