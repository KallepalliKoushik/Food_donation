# Generated by Django 5.2 on 2025-04-19 10:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Donations', '0015_deliveryrequest_expiry_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodbooking',
            name='booking_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
