# Generated by Django 2.2.3 on 2019-11-22 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riaapp', '0015_auto_20191122_1053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='req',
            name='indeg',
        ),
        migrations.RemoveField(
            model_name='req',
            name='outdeg',
        ),
        migrations.AddField(
            model_name='issue',
            name='text',
            field=models.CharField(default='Empty', max_length=2000),
        ),
        migrations.AlterField(
            model_name='req',
            name='text',
            field=models.CharField(max_length=200),
        ),
    ]
