# Generated by Django 4.1.6 on 2023-03-27 04:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0010_remove_student_is_active_student_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='active',
            new_name='is_active',
        ),
    ]
