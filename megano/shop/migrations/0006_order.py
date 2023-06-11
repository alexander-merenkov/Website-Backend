# Generated by Django 4.2.2 on 2023-06-11 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0032_alter_category_subcategories'),
        ('shop', '0005_rename_products_basketitem_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('fullName', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=16, verbose_name='phone number')),
                ('deliveryType', models.CharField(blank=True, max_length=20)),
                ('paymentType', models.CharField(blank=True, max_length=20)),
                ('totalCost', models.DecimalField(decimal_places=2, max_digits=8)),
                ('status', models.CharField(blank=True, max_length=20)),
                ('city', models.CharField(blank=True, max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('products', models.ManyToManyField(to='products.productfull')),
            ],
        ),
    ]
