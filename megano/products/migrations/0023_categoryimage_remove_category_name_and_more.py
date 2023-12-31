# Generated by Django 4.2 on 2023-06-08 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_remove_specifications_product_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src', models.URLField()),
                ('alt', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='category',
            name='name',
        ),
        migrations.AddField(
            model_name='category',
            name='subcategories',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.category'),
        ),
        migrations.AddField(
            model_name='category',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.category')),
                ('image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.categoryimage')),
            ],
            options={
                'verbose_name': 'Subcategory',
                'verbose_name_plural': 'Subcategories',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.categoryimage'),
        ),
    ]
