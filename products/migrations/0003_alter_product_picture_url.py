# Generated by Django 4.1.4 on 2022-12-25 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_alter_category_options_alter_category_parent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='picture_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
