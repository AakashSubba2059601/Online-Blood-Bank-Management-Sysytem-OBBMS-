# Generated by Django 4.0.3 on 2023-04-21 06:15

from django.db import migrations, models
import donor.models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0014_blooddonate_future_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blooddonate',
            name='future_date',
        ),
        migrations.AddField(
            model_name='blooddonate',
            name='date_90_days',
            field=models.DateField(default=donor.models.default_date_90_days),
        ),
    ]