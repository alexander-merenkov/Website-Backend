# Generated by Django 4.2 on 2023-06-06 21:26

from django.db import migrations, models
import django.db.models.deletion
import profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src', models.ImageField(blank=True, null=True, upload_to=profiles.models.avatar_uploads)),
                ('alt', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.avatar'),
        ),
    ]
