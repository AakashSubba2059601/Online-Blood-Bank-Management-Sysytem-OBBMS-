# Generated by Django 4.0.3 on 2023-05-04 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0022_alter_donor_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donor',
            name='mobile',
            field=models.CharField(max_length=10),
        ),
    ]
