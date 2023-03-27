# Generated by Django 4.1.6 on 2023-03-02 05:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_student_enrollment_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='student',
            name='last_name',
            field=models.CharField(default=datetime.datetime(2023, 3, 2, 5, 10, 42, 832678, tzinfo=datetime.timezone.utc), max_length=100),
            preserve_default=False,
        ),
    ]