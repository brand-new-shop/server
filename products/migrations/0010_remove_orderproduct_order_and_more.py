# Generated by Django 4.1.4 on 2023-05-01 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_remove_product_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='product',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderProduct',
        ),
    ]
