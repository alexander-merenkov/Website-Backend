# Generated by Django 4.2 on 2023-06-04 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_review_email_alter_review_rate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productfull',
            name='specifications',
            field=models.TextField(blank=True, max_length=100),
        ),
    ]