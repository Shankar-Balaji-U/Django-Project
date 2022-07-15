# Generated by Django 3.2.7 on 2022-03-01 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BillingSystem', '0006_auto_20220227_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='bill_total_amount',
            field=models.DecimalField(decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='invoiceitem',
            name='item_name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='invoiceitem',
            name='item_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='invoiceitem',
            name='item_quantity',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Quantity'),
        ),
        migrations.AlterField(
            model_name='invoiceitem',
            name='item_subtotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Sub Total'),
        ),
    ]