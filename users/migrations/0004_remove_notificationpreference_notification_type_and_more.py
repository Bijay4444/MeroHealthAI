# Generated by Django 5.1.5 on 2025-01-24 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_caregiverrelationship_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificationpreference',
            name='notification_type',
        ),
        migrations.AddField(
            model_name='notificationpreference',
            name='email',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='notificationpreference',
            name='push',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notificationpreference',
            name='sms',
            field=models.BooleanField(default=False),
        ),
    ]
