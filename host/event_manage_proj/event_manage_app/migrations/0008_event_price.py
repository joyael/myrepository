# Generated by Django 5.0.6 on 2024-09-06 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_manage_app', '0007_passwordresetorganizer'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
