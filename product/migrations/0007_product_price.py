# Generated by Django 5.0 on 2023-12-27 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_product_description_product_detail_product_slug_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
