# Generated by Django 2.2.3 on 2019-09-09 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('riaapp', '0005_auto_20190909_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dep',
            name='dep_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='riaapp.DepType'),
        ),
    ]