# Generated by Django 5.0.1 on 2024-04-07 07:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_alter_payment_payment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 7, 7, 52, 51, 194449, tzinfo=datetime.timezone.utc), verbose_name='Дата платежа'),
        ),
    ]