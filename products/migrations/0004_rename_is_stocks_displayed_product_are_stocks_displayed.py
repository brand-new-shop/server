# Generated by Django 4.1.4 on 2023-01-05 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_productpicture_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='is_stocks_displayed',
            new_name='are_stocks_displayed',
        ),
    ]
