# Generated by Django 2.2.3 on 2019-09-09 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('riaapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dep',
            name='dep_type',
        ),
        migrations.RemoveField(
            model_name='dep',
            name='destination',
        ),
        migrations.RemoveField(
            model_name='dep',
            name='source',
        ),
        migrations.RemoveField(
            model_name='deplearninstance',
            name='dep',
        ),
        migrations.DeleteModel(
            name='DepType',
        ),
        migrations.DeleteModel(
            name='NLPDoc',
        ),
        migrations.RemoveField(
            model_name='path',
            name='deps',
        ),
        migrations.RemoveField(
            model_name='req',
            name='nlp_doc',
        ),
        migrations.DeleteModel(
            name='Dep',
        ),
        migrations.DeleteModel(
            name='DepLearnInstance',
        ),
        migrations.DeleteModel(
            name='Path',
        ),
        migrations.DeleteModel(
            name='Req',
        ),
    ]
