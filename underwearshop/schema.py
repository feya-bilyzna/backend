# cookbook/schema.py
import graphene
from graphene_django import DjangoObjectType

from underwearshop.models import (
    Product,
    ProductImage,
    ProductRemains,
    Category,
)
from django.utils.translation import gettext_lazy as _

PRODUCT_PREFETCHES = (
    'images',
    'remains',
    'remains__productvariant',
    'categories',
)


class ProductType(DjangoObjectType):

    class Meta:

        model = Product
        fields = (
            "id",
            "name",
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
            "remains",
            "price",
        )

    variant_id = graphene.Int()
    variant_name = graphene.String()

    @staticmethod
    def resolve_variant_id(root, info, **kwargs):
        return root.productvariant.id

    @staticmethod
    def resolve_variant_name(root, info, **kwargs):
        return root.productvariant.name


class Query(graphene.ObjectType):

    all_products = graphene.List(ProductType)
    category_products = graphene.List(
        ProductType, category_name=graphene.String(required=True)
    )
    product_by_id = graphene.Field(ProductType, id=graphene.Int(required=True))

    def resolve_all_products(root, info):

        return Product.objects.prefetch_related(*PRODUCT_PREFETCHES).all()

    def resolve_category_products(root, info, category_name):

        try:
            return Category.objects.get(
                name=category_name
            ).products.prefetch_related(*PRODUCT_PREFETCHES).all()
        except Category.DoesNotExist:
            return []

    def resolve_product_by_id(root, info, id):

        try:
            return Product.objects.prefetch_related(
                *PRODUCT_PREFETCHES
            ).get(id=id)

        except Product.DoesNotExist:
            return None


schema = graphene.Schema(
    query=Query,
)
