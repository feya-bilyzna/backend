# Generated by Django 3.2.4 on 2022-02-13 11:27

from django.db import migrations


def delete_log_entries(apps, schema_editor):

    LogEntry = apps.get_model('admin', 'LogEntry')
    LogEntry.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('underwearshop', '0014_auto_20210902_0615'),
    ]

    operations = [
        migrations.RunPython(
            delete_log_entries, reverse_code=migrations.RunPython.noop
        ),
    ]
