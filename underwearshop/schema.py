# cookbook/schema.py
import graphene
from graphene_django import DjangoObjectType

from underwearshop.models import Product, ProductImage


class ProductType(DjangoObjectType):

    class Meta:

        model = Product
        fields = (
            "id",
            "name",
            "description",
            "images",
        )


class ProductImageType(DjangoObjectType):

    class Meta:

        model = ProductImage
        fields = (
            "id",
            "product",
            "url",
        )


class Query(graphene.ObjectType):

    all_products = graphene.List(ProductType)
    category_products = graphene.List(
        ProductType, category_name=graphene.String(required=True)
    )
    product_by_id = graphene.Field(ProductType, id=graphene.Int(required=True))

    def resolve_all_products(root, info):

        return Product.objects.prefetch_related('images').all()

    def resolve_category_products(root, info, category_name):

        return Product.objects.prefetch_related('images').filter(
            category__name=category_name
        )

    def resolve_product_by_id(root, info, id):

        try:
            return Product.objects.prefetch_related('images').get(id=id)

        except Product.DoesNotExist:
            return None


schema = graphene.Schema(
    query=Query,
)
