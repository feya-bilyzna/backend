from django.db import models
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


class Category(models.Model):

    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name=_('Name'),
    )
    parent_prefix = models.CharField(
        max_length=128,
        verbose_name=_('Parent prefix'),
        default=gettext('Uncategorized')
    )

    def __str__(self):

        return self.name

    class Meta:

        verbose_name = _('Product category')
        verbose_name_plural = _('Product categories')


class ProductVariant(models.Model):

    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name=_('Name'),
    )
    style = models.JSONField(
        default=dict,
        verbose_name=_('Style'),
    )

    def __str__(self):

        return self.name

    class Meta:

        verbose_name = _('Product variant')
        verbose_name_plural = _('Product variants')


class Product(models.Model):

    vendor_code = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name=_('Vendor code'),
        default=gettext('Test-product'),
    )
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
        related_name='products',
        verbose_name=_('variant'),
    )
    categories = models.ManyToManyField(
        Category,
        related_name='products',
        verbose_name=_('categories'),
    )
    image_links = models.JSONField(
        default=list,
        verbose_name=_('Image links'),
    )

    def __str__(self):

        return self.name

    class Meta:

        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class ProductRemains(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='remains',
        verbose_name=_('product'),
    )
    productvariant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        verbose_name=_('variant'),
    )
    remains = models.PositiveSmallIntegerField(
        default=1,
        verbose_name=_('Remains amount'),
    )
    price = models.FloatField(
        verbose_name=_('Price'),
        validators=[MinValueValidator(0.01)],
    )

    def __str__(self):

        return _('Remains: %(product)s (%(variant)s)') % {
            'product': self.product.name, 'variant': self.productvariant.name
        }

    class Meta:

        verbose_name = _('Product remains relation')
        verbose_name_plural = _('Product remains relations')
        unique_together = ['product', 'productvariant']


class Customer(models.Model):

    contact_info = models.CharField(
        max_length=128,
        unique=True,
        verbose_name=_('Contact info'),
    )

    def __str__(self):

        return self.contact_info

    class Meta:

        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')


class Order(models.Model):

    customer = models.ForeignKey(
        Customer,
        null=True,
        on_delete=models.SET_NULL,
        related_name='orders',
        verbose_name=_('customer'),
    )
    positions = models.ManyToManyField(
        ProductRemains,
        through='OrderProduct',
        verbose_name=_('related product remains'),
    )
    processed = models.BooleanField(
        verbose_name=_('Order processed'),
        default=False,
    )

    def __str__(self):

        return _('Order #%(number)s') % {
            'number': self.id,
        }

    class Meta:

        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class OrderProduct(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='orderproducts',
        verbose_name=_('order'),
    )
    productremains = models.ForeignKey(
        ProductRemains,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('related product remains'),
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        verbose_name=_('Product amount'),
    )

    class Meta:

        verbose_name = _('Order position')
        verbose_name_plural = _('Order positions')
