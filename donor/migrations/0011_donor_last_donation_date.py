# Generated by Django 4.0.3 on 2023-04-19 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0010_stock_remove_blooddonate_blood_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='donor',
            name='last_donation_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
