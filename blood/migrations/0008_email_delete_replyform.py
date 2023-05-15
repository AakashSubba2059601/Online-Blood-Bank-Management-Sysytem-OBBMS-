# Generated by Django 4.0.3 on 2023-05-02 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood', '0007_replyform'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('sent_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='ReplyForm',
        ),
    ]
