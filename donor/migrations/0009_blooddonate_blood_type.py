# Generated by Django 4.0.3 on 2023-04-18 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0008_blooddonate_hemoglobin_blooddonate_sex_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blooddonate',
            name='blood_type',
            field=models.CharField(default='', max_length=10),
        ),
    ]