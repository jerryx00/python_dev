# Generated by Django 2.1.1 on 2018-11-13 03:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0011_auto_20181113_0906'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('title', models.CharField(max_length=30)),
                ('authors', models.ManyToManyField(to='news.Author')),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='Publication',
        ),
        migrations.AlterField(
            model_name='account',
            name='userinfo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='news.Userinfo'),
        ),
        migrations.AlterField(
            model_name='article',
            name='publications',
            field=models.ManyToManyField(to='news.Publisher'),
        ),
        migrations.AddField(
            model_name='book',
            name='pub',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.Publisher'),
        ),
    ]
