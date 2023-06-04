# Generated by Django 4.2 on 2023-06-04 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_category_options_review_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='rate',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(blank=True),
        ),
    ]
