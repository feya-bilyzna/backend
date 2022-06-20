from django.db import migrations
from collections import defaultdict

def convert_images_to_json(apps, schema_editor):

    Product = apps.get_model('underwearshop', 'Product')
    ProductImage = apps.get_model('underwearshop', 'ProductImage')
    images_data = ProductImage.objects.values('product__id', 'url')
    images_dict = defaultdict(list)
    for image in images_data:
        images_dict[image['product__id']].append(image['url'])

    products = Product.objects.all()
    for product in products:
        product.image_links = images_dict[product.id]
    Product.objects.bulk_update(products, ['image_links'])

def convert_json_to_images(apps, schema_editor):

    Product = apps.get_model('underwearshop', 'Product')
    ProductImage = apps.get_model('underwearshop', 'ProductImage')

    ProductImage.objects.all().delete()
    ProductImage.objects.bulk_create([
        ProductImage(
            product=product,
            url=url,
        )
        for product in Product.objects.all()
        for url in product.image_links
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('underwearshop', '0018_product_image_links'),
    ]

    operations = [
        migrations.RunPython(
            convert_images_to_json,
            reverse_code=convert_json_to_images,
        ),
    ]
