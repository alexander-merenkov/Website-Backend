# Generated by Django 4.2.2 on 2023-06-11 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_alter_order_totalcost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='createdAt',
            field=models.DateTimeField(null=True),
        ),
    ]
