from modeltranslation.translator import register, TranslationOptions
from .models import Product, ProductVariant


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(ProductVariant)
class ProductVariantTranslationOptions(TranslationOptions):
    fields = ('name', )
