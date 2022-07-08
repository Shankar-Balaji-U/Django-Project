# Generated by Django 3.2.7 on 2022-04-30 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_account', models.CharField(blank=True, editable=False, max_length=18)),
                ('to_account', models.CharField(blank=True, editable=False, max_length=18)),
                ('transaction_id', models.CharField(blank=True, max_length=30)),
                ('sender', models.CharField(blank=True, max_length=264, null=True)),
                ('payment_method', models.CharField(blank=True, choices=[('UPI', 'UPI'), ('Cash', 'Cash'), ('Check', 'Check'), ('Debit cards', 'Debit cards'), ('Credit cards', 'Credit cards'), ('Internet Banking', 'Internet Banking')], max_length=264, null=True)),
                ('amount', models.IntegerField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]