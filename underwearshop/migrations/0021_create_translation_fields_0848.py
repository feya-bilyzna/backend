# Generated by Django 3.2.4 on 2022-06-23 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('underwearshop', '0020_delete_productimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='product',
            name='description_uk',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='name_ru',
            field=models.CharField(max_length=128, null=True, unique=True, verbose_name='Name'),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='name_uk',
            field=models.CharField(max_length=128, null=True, unique=True, verbose_name='Name'),
        ),
    ]