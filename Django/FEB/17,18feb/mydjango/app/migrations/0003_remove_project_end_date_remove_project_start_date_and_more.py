# Generated by Django 5.1.5 on 2025-02-18 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='project',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='project',
            name='status',
        ),
    ]
