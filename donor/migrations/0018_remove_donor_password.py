# Generated by Django 4.0.3 on 2023-04-29 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0017_contact_remove_chatmember_chat_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donor',
            name='password',
        ),
    ]
