# Generated by Django 5.0.6 on 2024-09-10 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_manage_app', '0009_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ticketprice',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
