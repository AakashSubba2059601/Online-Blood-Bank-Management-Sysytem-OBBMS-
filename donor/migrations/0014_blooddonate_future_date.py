# Generated by Django 4.0.3 on 2023-04-20 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0013_remove_donor_last_donation_date_donor_last_donation'),
    ]

    operations = [
        migrations.AddField(
            model_name='blooddonate',
            name='future_date',
            field=models.DateField(null=True),
        ),
    ]