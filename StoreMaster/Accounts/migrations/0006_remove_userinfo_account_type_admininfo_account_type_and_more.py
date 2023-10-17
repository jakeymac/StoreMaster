# Generated by Django 4.2.5 on 2023-10-17 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0005_userinfo_account_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='account_type',
        ),
        migrations.AddField(
            model_name='admininfo',
            name='account_type',
            field=models.CharField(default='admin', max_length=15),
        ),
        migrations.AddField(
            model_name='customerinfo',
            name='account_type',
            field=models.CharField(default='customer', max_length=15),
        ),
        migrations.AddField(
            model_name='employeeinfo',
            name='account_type',
            field=models.CharField(default='employee', max_length=15),
        ),
        migrations.AddField(
            model_name='managerinfo',
            name='account_type',
            field=models.CharField(default='manager', max_length=15),
        ),
    ]
