# Generated by Django 4.2 on 2023-06-08 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0029_alter_categoryimage_src'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryimage',
            name='src',
            field=models.ImageField(upload_to='categoryimages/'),
        ),
    ]
