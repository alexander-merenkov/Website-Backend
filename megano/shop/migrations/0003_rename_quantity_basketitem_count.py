# Generated by Django 4.2.2 on 2023-06-11 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_remove_basket_count_remove_basket_products_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basketitem',
            old_name='quantity',
            new_name='count',
        ),
    ]
