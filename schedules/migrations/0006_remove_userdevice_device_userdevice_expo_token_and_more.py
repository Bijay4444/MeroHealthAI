# Generated by Django 5.1.5 on 2025-02-17 16:19

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0005_userdevice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdevice',
            name='device',
        ),
        migrations.AddField(
            model_name='userdevice',
            name='expo_token',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userdevice',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
