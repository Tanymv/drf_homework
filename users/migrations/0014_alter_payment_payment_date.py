# Generated by Django 5.0.1 on 2024-03-20 09:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_payment_payment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 9, 1, 50, 137719, tzinfo=datetime.timezone.utc), verbose_name='Дата платежа'),
        ),
    ]
