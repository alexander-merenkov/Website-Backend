# Generated by Django 4.2 on 2023-06-17 14:41

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0032_alter_category_subcategories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='src',
            field=models.ImageField(blank=True, null=True, upload_to=products.models.product_image_upload),
        ),
    ]