# Generated by Django 3.2.7 on 2022-05-03 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BillingSystem', '0014_alter_customer_industry_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='industry_name',
            field=models.CharField(default='Retail Customer', max_length=50),
        ),
    ]
