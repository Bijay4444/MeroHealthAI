# Generated by Django 5.1.5 on 2025-03-07 04:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medications', '0003_medication_created_at_schedule_is_active_and_more'),
        ('schedules', '0006_remove_userdevice_device_userdevice_expo_token_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reminder',
            unique_together={('schedule', 'sent_time')},
        ),
    ]
