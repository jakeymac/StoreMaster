# Generated by Django 4.2.5 on 2023-12-11 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Stores', '0001_initial'),
        ('Orders', '0002_remove_order_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Stores.store'),
        ),
    ]
