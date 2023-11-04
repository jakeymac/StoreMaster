# Generated by Django 4.2.5 on 2023-10-17 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0007_remove_admininfo_account_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='account_type',
            field=models.CharField(choices=[('customer', 'Customer'), ('employee', 'Employee'), ('manager', 'Manager'), ('admin', 'Admin')], default='employee', max_length=15),
        ),
    ]