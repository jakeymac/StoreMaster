# Generated by Django 4.2.5 on 2023-12-11 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0004_managerinfo_stock_notifications'),
        ('Purchases', '0005_alter_purchase_admin_id_alter_purchase_customer_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='admin_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin', to='Accounts.admininfo'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='employee_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='Accounts.employeeinfo'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='manager_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='manager', to='Accounts.managerinfo'),
        ),
    ]
