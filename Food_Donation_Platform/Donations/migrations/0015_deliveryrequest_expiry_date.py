# Generated by Django 5.2 on 2025-04-19 06:50

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Donations', '0014_deliveryrequest_food_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryrequest',
            name='expiry_date',
            field=models.DateField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]
