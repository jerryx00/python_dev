# Generated by Django 2.1.1 on 2018-11-14 00:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0012_auto_20181113_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='mobiel',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='userinfo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='news.Userinfo'),
        ),
    ]
