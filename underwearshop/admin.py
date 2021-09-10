from django.contrib import admin
from .models import (
    Order,
    Product,
    ProductRemains,
    ProductVariant,
    ProductImage,
    OrderProduct,
    Category,
    Customer,
)
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django import forms
from django.urls import reverse
from django.db.models import Sum, functions, F


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
    autocomplete_fields = ('productremains',)
    readonly_fields = ('get_product_price',)
    min_num = 1
    extra = 0

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('productremains')

    def get_product_price(self, obj):

        return obj.productremains.price

    get_product_price.short_description = _('Price')


class ProductRemainsInline(admin.TabularInline):
    model = ProductRemains
    autocomplete_fields = ('productvariant',)
    min_num = 1
    extra = 0


class ProductImageInline(admin.StackedInline):
    model = ProductImage


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderPositionsInline,
    ]
    autocomplete_fields = ('customer',)
    search_fields = ('customer__contact_info', 'id')
    list_display = ('id', 'get_contact_info', 'processed')
    readonly_fields = ('get_total_price',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('customer')

    def get_contact_info(self, obj):

        if obj.customer is None:
            return None

        return format_html(
            "<a href='{url}'>{text}</a>",
            url=reverse(
                'admin:underwearshop_customer_change', args=(obj.customer.id,)
            ),
            text=obj.customer.contact_info,
        )

    get_contact_info.short_description = _('Customer')

    def get_total_price(self, obj):

        return obj.orderproducts.aggregate(
            total=Sum(F('amount') * F('productremains__price'))
        )['total']

    get_total_price.short_description = _('Total price')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    inlines = [
        ProductRemainsInline,
        ProductImageInline,
    ]
    search_fields = ('name', 'id')
    autocomplete_fields = ('categories',)
    list_display = ('name', 'get_total_remains',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            total_remains=functions.Coalesce(Sum('remains__remains'), 0)
        )

    def get_total_remains(self, obj):

        return obj.total_remains

    get_total_remains.admin_order_field  = 'total_remains'
    get_total_remains.short_description = _('Total remains')


@admin.register(ProductRemains)
class ProductRemainsAdmin(admin.ModelAdmin):
    autocomplete_fields = ('product', 'productvariant')
    search_fields = ('product__name', 'productvariant__name')


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    inlines = [
        ProductRemainsInline,
    ]
    search_fields = ('name', 'id')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_order')
    autocomplete_fields = ('order', 'productremains',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('order')

    def get_order(self, obj):

        return format_html(
            "<a href='{url}'>{text}</a>",
            url=reverse(
                'admin:underwearshop_order_change', args=(obj.order.id,)
            ),
            text=obj.order.id,
        )

    get_order.short_description = _('Order')
    get_order.admin_order_field  = 'order__id'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_prefix')
    search_fields = ('name',)


class OrderInline(admin.TabularInline):
    model = Order
    extra = 0
    max_num = 0
    show_change_link = True


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('contact_info',)
    search_fields = ('contact_info',)
    inlines = (OrderInline,)
