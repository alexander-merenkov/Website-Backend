# Generated by Django 4.2 on 2023-06-04 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_productfull_specifications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productfull',
            name='rating',
            field=models.FloatField(null=True),
        ),
    ]