from django.contrib import admin
from .models import (
    Order,
    Product,
    ProductRemains,
    ProductVariant,
    ProductImage,
    OrderProduct
)


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
    inlines = [
        ProductVariantInline,
        ProductImageInline,
    ]


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
