# Generated by Django 3.2.4 on 2022-04-05 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('underwearshop', '0015_deleting_log_entries'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_links',
            field=models.JSONField(default=list, verbose_name='Image links'),
        ),
    ]
