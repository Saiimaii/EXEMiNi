# Generated by Django 5.0.6 on 2024-10-04 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myshop', '0002_datashop_payments_status_datashop_products_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datashop',
            name='payments_status',
            field=models.CharField(choices=[('รอร้านตรวจสอบ', 'Checked'), ('รอการชำระเงิน', 'Pending'), ('ชำระเงินเรียบร้อยแล้ว', 'Paid')], default='รอร้านตรวจสอบ', max_length=50, verbose_name='การชำระเงิน'),
        ),
    ]
