# Generated by Django 2.1.2 on 2018-11-03 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OpsLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_ip', models.CharField(max_length=32)),
                ('hostname', models.CharField(max_length=64, null=True)),
                ('user_name', models.CharField(max_length=64)),
                ('start_time', models.CharField(max_length=64)),
                ('audit_log', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UserLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=32)),
                ('ready_name', models.CharField(max_length=32)),
                ('url_title', models.CharField(max_length=64)),
                ('status', models.CharField(max_length=32)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
