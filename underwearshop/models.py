from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class ProductVariant(models.Model):

    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name=_('Name'),
    )

    class Meta:

        verbose_name = _('Product variant')
        verbose_name_plural = _('Product variants')


class Product(models.Model):

    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name=_('Name'),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description'),
    )
    variants = models.ManyToManyField(
        ProductVariant,
        through='ProductRemains',
        related_name=_('variants'),
        verbose_name=_('variant'),
    )

    class Meta:

        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class ProductRemains(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name=_('products'),
        verbose_name=_('product'),
    )
    productvariant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        verbose_name=_('variant'),
    )
    remains = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_('Remains amount'),
    )
    price = models.PositiveIntegerField(
        verbose_name=_('Price'),
    )

    class Meta:

        verbose_name = _('Product remains relation')
        verbose_name_plural = _('Product remains relations')


class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('product'),
        related_name=_('images'),
    )
    url = models.URLField(
        verbose_name=_('Link to image'),
    )

    class Meta:

        verbose_name = _('Product image')
        verbose_name_plural = _('Product images')


class Order(models.Model):

    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name=_('users'),
        verbose_name=_('user'),
    )
    positions = models.ManyToManyField(
        ProductRemains,
        through='OrderProduct',
        verbose_name=_('related product remains'),
    )

    class Meta:

        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class OrderProduct(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name=_('orders'),
        verbose_name=_('order'),
    )
    productremains = models.ForeignKey(
        ProductRemains,
        on_delete=models.CASCADE,
        verbose_name=_('related product remains'),
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        verbose_name=_('Product amount'),
    )

    class Meta:

        verbose_name = _('Order position')
        verbose_name_plural = _('Order positions')
