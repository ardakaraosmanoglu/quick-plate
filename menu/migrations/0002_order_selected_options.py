# Generated by Django 5.0.6 on 2024-05-16 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='selected_options',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
