# Generated by Django 3.2.4 on 2021-08-28 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('underwearshop', '0012_auto_20210824_2314'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='vendor_code',
            field=models.CharField(blank=True, default='Тест-товар', max_length=128, null=True, verbose_name='Vendor code'),
        ),
    ]
