# Generated by Django 5.0 on 2023-12-27 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_rename_create_at_category_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default=1, upload_to='ProductsImages/'),
            preserve_default=False,
        ),
    ]
