# Generated by Django 4.0.3 on 2023-05-04 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood', '0015_alter_bloodrequest_requisition_form'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodrequest',
            name='requisition_form',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pic/Donor/'),
        ),
    ]