# Generated by Django 2.1.2 on 2018-11-03 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_log', '0002_auto_20181103_2118'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserLog1',
            new_name='UserLog',
        ),
    ]