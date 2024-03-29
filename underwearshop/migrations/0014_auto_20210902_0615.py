# Generated by Django 3.2.4 on 2021-09-02 03:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('underwearshop', '0013_product_vendor_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_info', models.CharField(max_length=128, unique=True, verbose_name='Contact info')),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.AddField(
            model_name='order',
            name='processed',
            field=models.BooleanField(default=False, verbose_name='Order processed'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='productremains',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='underwearshop.productremains', verbose_name='related product remains'),
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='underwearshop.customer', verbose_name='customer'),
        ),
    ]
