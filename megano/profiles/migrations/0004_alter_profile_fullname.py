# Generated by Django 4.2 on 2023-06-07 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_rename_full_name_profile_fullname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='fullName',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
