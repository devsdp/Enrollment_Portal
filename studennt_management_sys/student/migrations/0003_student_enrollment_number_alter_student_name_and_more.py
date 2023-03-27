# Generated by Django 4.1.7 on 2023-02-20 12:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_remove_student_programs_student_program_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='enrollment_number',
            field=models.CharField(default=datetime.datetime(2023, 2, 20, 12, 19, 44, 266964, tzinfo=datetime.timezone.utc), editable=False, max_length=10, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='student',
            name='program',
            field=models.CharField(max_length=30),
        ),
    ]