# Generated by Django 4.2.2 on 2023-06-10 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0031_remove_productfull_category_productfull_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='subcategories',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.category'),
        ),
    ]