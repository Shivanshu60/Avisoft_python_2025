# Generated by Django 5.1.5 on 2025-02-18 10:18

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_project_end_date_remove_project_start_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(default='Pending', max_length=50),
        ),
    ]
