# Generated by Django 4.0.3 on 2023-04-20 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0011_donor_last_donation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donor',
            name='last_donation_date',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
