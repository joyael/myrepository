# Generated by Django 5.0.6 on 2024-10-04 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_manage_app', '0014_event_isrefunded_event_refunddate_event_refundid'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='refundprice',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
