# Generated by Django 3.2.4 on 2021-08-10 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('underwearshop', '0008_transfering_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(related_name='products', to='underwearshop.Category', verbose_name='categories'),
        ),
    ]
