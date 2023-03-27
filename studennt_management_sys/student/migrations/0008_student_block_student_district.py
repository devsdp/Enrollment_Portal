# Generated by Django 4.1.6 on 2023-03-02 05:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_student_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='block',
            field=models.CharField(default=datetime.datetime(2023, 3, 2, 5, 25, 53, 522763, tzinfo=datetime.timezone.utc), max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='district',
            field=models.CharField(default=datetime.datetime(2023, 3, 2, 5, 26, 7, 530556, tzinfo=datetime.timezone.utc), max_length=100),
            preserve_default=False,
        ),
    ]