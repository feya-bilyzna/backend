# Generated by Django 3.2.4 on 2021-08-10 14:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('underwearshop', '0005_auto_20210710_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='parent_prefix',
            field=models.CharField(default='Без категории', max_length=128, verbose_name='Parent prefix'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderproducts', to='underwearshop.order', verbose_name='order'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='underwearshop.category', verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='variants',
            field=models.ManyToManyField(related_name='products', through='underwearshop.ProductRemains', to='underwearshop.ProductVariant', verbose_name='variant'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='underwearshop.product', verbose_name='product'),
        ),
        migrations.AlterField(
            model_name='productremains',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remains', to='underwearshop.product', verbose_name='product'),
        ),
    ]