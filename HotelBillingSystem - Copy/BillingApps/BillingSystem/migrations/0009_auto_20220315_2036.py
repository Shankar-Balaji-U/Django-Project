# Generated by Django 3.2.7 on 2022-03-15 15:06

import djangocustom.models.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BillingSystem', '0008_alter_invoice_bill_total_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='bill_total_amount',
        ),
        migrations.AlterField(
            model_name='invoiceitem',
            name='item_price',
            field=models.DecimalField(decimal_places=2, max_digits=20, validators=[djangocustom.models.validators.NonZeroValidator], verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='invoiceitem',
            name='item_quantity',
            field=models.DecimalField(decimal_places=2, max_digits=20, validators=[djangocustom.models.validators.NonZeroValidator], verbose_name='Quantity'),
        ),
    ]