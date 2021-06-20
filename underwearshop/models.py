from django.db import models
from django.contrib.auth.models import User


class ProductVariant(models.Model):

    name = models.CharField(max_length=128, unique=True)


class Product(models.Model):

    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    variants = models.ManyToManyField(ProductVariant, through='ProductRemains')


class ProductRemains(models.Model):

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE
    )
    productvariant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE
    )
    remains = models.PositiveSmallIntegerField(default=0)
    price = models.PositiveIntegerField()

    class Meta:

        verbose_name = 'Product remains relation'
        verbose_name_plural = 'Product remains relations'


class ProductImage(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    url = models.URLField()


class Order(models.Model):

    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    positions = models.ManyToManyField(ProductRemains, through='OrderProduct')


class OrderProduct(models.Model):

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE
    )
    productremains = models.ForeignKey(
        ProductRemains, on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(default=1)

    class Meta:

        verbose_name = 'Order position'
        verbose_name_plural = 'Order positions'
