# Generated by Django 4.2 on 2023-06-06 21:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_avatar_alter_profile_avatar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='full_name',
            new_name='fullName',
        ),
    ]
