# cookbook/schema.py
import graphene
from graphene_django import DjangoObjectType
from graphene.types.generic import GenericScalar
from graphql import GraphQLError

from underwearshop.models import (
    Product,
    ProductImage,
    ProductRemains,
    Customer,
    Order,
    OrderProduct,
)

from django.db.models import When, Case, Value, Sum, Min, Q

from django.utils.translation import gettext_lazy as _

PRODUCT_PREFETCHES = (
    'images',
    'remains',
    'remains__productvariant',
    'categories',
)
ORDERPRODUCT_PRODUCT_RELATION = 'productremains__product'
ORDERPRODUCT_PREFETCHES = tuple(
    f'{ORDERPRODUCT_PRODUCT_RELATION}__{prefetch}'
    for prefetch in PRODUCT_PREFETCHES
)


class ProductType(DjangoObjectType):

    class Meta:

        model = Product
        fields = (
            "id",
            "name",
            "vendor_code",
            "description",
            "images",
            "remains",
        )

    brand_name = graphene.String()
    categories = graphene.List(graphene.String)

    @staticmethod
    def resolve_brand_name(root, info, **kwargs):
        for category in root.categories.all():
            if category.parent_prefix == _('Brands'):
                return category.name
        return None

    @staticmethod
    def resolve_categories(root, info, **kwargs):
        return root.categories.all()


class OrderProductType(DjangoObjectType):

    class Meta:

        model = OrderProduct
        fields = (
            'id',
            'amount',
            'productremains',
        )

    product = graphene.Field(ProductType)

    @staticmethod
    def resolve_product(root, info, **kwargs):

        return root.productremains.product


class OrderType(DjangoObjectType):

    class Meta:

        model = Order
        fields = (
            "id",
            "processed"
        )

    positions = graphene.List(OrderProductType)

    @staticmethod
    def resolve_positions(root, info, **kwargs):

        return OrderProduct.objects.select_related(
            'productremains',
            ORDERPRODUCT_PRODUCT_RELATION,
        ).prefetch_related(
            'productremains__productvariant',
            *ORDERPRODUCT_PREFETCHES
        ).filter(order=root)


class ProductImageType(DjangoObjectType):

    class Meta:

        model = ProductImage
        fields = (
            "id",
            "product",
            "url",
        )


class ProductRemainsType(DjangoObjectType):

    class Meta:

        model = ProductRemains
        fields = (
            "id",
            "remains",
            "price",
        )

    variant_id = graphene.Int()
    variant_name = graphene.String()
    variant_style = GenericScalar()

    @staticmethod
    def resolve_variant_id(root, info, **kwargs):
        return root.productvariant.id

    @staticmethod
    def resolve_variant_name(root, info, **kwargs):
        return root.productvariant.name

    @staticmethod
    def resolve_variant_style(root, info, **kwargs):
        return root.productvariant.style


def slice_products(qs, page, order_by=()):

    return qs.annotate(
        product_remains=Sum('remains__remains')
    ).annotate(
        in_stock=Case(
            When(product_remains__gt=0, then=Value(True)),
            default=Value(False)
        ),
        price=Min('remains__price'),
    ).order_by(
        *order_by, '-in_stock', '-id',
    )[(page-1)*12:page*12]


class OrderItem(graphene.InputObjectType):

    remains_id = graphene.Int(required=True)
    amount = graphene.Int(required=True)


class MakeOrder(graphene.Mutation):

    class Arguments:

        contact_info = graphene.String(required=True)
        orders_list = graphene.List(OrderItem, required=True)

    result = graphene.String()

    def mutate(root, info, contact_info, orders_list):

        if len(orders_list) > 20:
            return MakeOrder(result='ORDER TOO LARGE')

        orders = set()
        for order in orders_list:
            if order.remains_id in orders:
                raise GraphQLError('Remains id must be unique.')
            orders.add(order.remains_id)

        try:
            customer = Customer.objects.get(contact_info=contact_info)
        except Customer.DoesNotExist:
            customer = Customer(contact_info=contact_info)
            customer.save()

        order = Order.objects.filter(
            customer=customer, processed=False
        ).order_by('id').first()
        created = False
        if order is None:
            order = Order(customer=customer, processed=False)
            created = True

        valid_remains = dict(ProductRemains.objects.filter(
            id__in=orders
        ).values_list('id', 'remains'))
        positions = [
            OrderProduct(
                order=order,
                productremains_id=order_item['remains_id'],
                amount=order_item['amount']
            ) for order_item in orders_list
            if valid_remains.get(
                order_item['remains_id'], 0
            ) >= order_item['amount']
        ]

        if len(positions) != len(orders_list):
            return MakeOrder(result='REMAINS INCONSISTENCY ERROR')

        if not positions:
            order.delete()
            return MakeOrder(result='DELETED')

        if created:
            order.save()

        OrderProduct.objects.filter(order=order).delete()
        OrderProduct.objects.bulk_create(positions)

        return MakeOrder(result='CREATED' if created else 'UPDATED')


class Mutation(graphene.ObjectType):

    make_order = MakeOrder.Field()


class ProductOrderBy(graphene.Enum):

    CHEAPEST = 1
    EXPENSIVE = 2


class Query(graphene.ObjectType):

    all_products = graphene.List(
        ProductType,
        page=graphene.Int(),
    )
    category_products = graphene.List(
        ProductType,
        category_name=graphene.List(graphene.String, required=True),
        variant_styles=GenericScalar(),
        order_by=ProductOrderBy(),
        page=graphene.Int(),
    )
    product_by_id = graphene.Field(
        ProductType,
        id=graphene.Int(required=True),
    )
    products_by_ids = graphene.List(
        ProductType,
        ids=graphene.List(graphene.Int, required=True),
    )
    order_by_contactinfo = graphene.Field(
        OrderType,
        contact_info=graphene.String(),
    )

    def resolve_all_products(root, info, page=1):

        return slice_products(
            Product.objects.prefetch_related(*PRODUCT_PREFETCHES).all(), page,
        )

    def resolve_category_products(
        root, info, category_name, variant_styles=None, order_by=None, page=1,
    ):

        products = Product.objects.prefetch_related(*PRODUCT_PREFETCHES)

        for category in category_name:
            products = products.filter(categories__name=category)

        if variant_styles:
            color = variant_styles.pop("color", None)
            appropriate_remains = ProductRemains.objects.filter(**{
                f'productvariant__style__{style}': value
                for style, value in variant_styles.items()
            })
            if color is not None:
                appropriate_remains = appropriate_remains.filter(
                    Q(productvariant__style__color=color) |
                    Q(productvariant__style__color__startswith=f'{color} ')
                )
            products = products.filter(
                id__in=appropriate_remains.distinct().values_list(
                    'product_id', flat=True
                )
            )

        return slice_products(
            products, page, [
                'price' if order_by == ProductOrderBy.CHEAPEST else '-price'
            ] if order_by else ()
        )

    def resolve_product_by_id(root, info, id):

        try:
            return Product.objects.prefetch_related(
                *PRODUCT_PREFETCHES
            ).get(id=id)

        except Product.DoesNotExist:
            return None

    def resolve_products_by_ids(root, info, ids):

        return Product.objects.prefetch_related(
            *PRODUCT_PREFETCHES
        ).filter(id__in=ids)

    def resolve_order_by_contactinfo(root, info, contact_info):

        return Order.objects.filter(
            customer__contact_info=contact_info, processed=False
        ).order_by('id').first()


schema = graphene.Schema(
    query=Query, mutation=Mutation
)
