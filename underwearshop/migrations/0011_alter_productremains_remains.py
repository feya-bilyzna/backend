# Generated by Django 3.2.4 on 2021-08-24 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('underwearshop', '0010_productvariant_style'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productremains',
            name='remains',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Remains amount'),
        ),
    ]
