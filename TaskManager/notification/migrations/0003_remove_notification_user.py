# Generated by Django 5.2.1 on 2025-06-11 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_rename_task_id_notification_task_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='user',
        ),
    ]
