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
    product_by_id = graphene.Field(ProductType, id=graphene.Int(required=True))

    def resolve_all_products(root, info):

        return Product.objects.all()

    def resolve_product_by_id(root, info, id):

        try:
            return Product.objects.get(id=id)

        except Product.DoesNotExist:
            return None


schema = graphene.Schema(
    query=Query,
)
