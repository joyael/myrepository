# Generated by Django 5.0.6 on 2024-08-29 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_manage_app', '0004_event_status_event_statusreason'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='approveddate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
