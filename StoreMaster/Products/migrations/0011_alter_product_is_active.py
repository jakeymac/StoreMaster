# Generated by Django 5.0.3 on 2024-03-26 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0010_product_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
