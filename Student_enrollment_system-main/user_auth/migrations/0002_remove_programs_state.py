# Generated by Django 4.1.5 on 2023-04-09 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programs',
            name='state',
        ),
    ]
