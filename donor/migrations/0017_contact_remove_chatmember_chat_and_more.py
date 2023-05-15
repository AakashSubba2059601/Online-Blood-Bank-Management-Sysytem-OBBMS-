# Generated by Django 4.0.3 on 2023-04-28 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0016_chat_message_chatmember'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=13)),
                ('email', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('timeStamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='chatmember',
            name='chat',
        ),
        migrations.RemoveField(
            model_name='chatmember',
            name='user',
        ),
        migrations.RemoveField(
            model_name='message',
            name='chat',
        ),
        migrations.RemoveField(
            model_name='message',
            name='sender',
        ),
        migrations.DeleteModel(
            name='Chat',
        ),
        migrations.DeleteModel(
            name='ChatMember',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]