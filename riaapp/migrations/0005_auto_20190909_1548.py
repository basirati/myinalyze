# Generated by Django 2.2.3 on 2019-09-09 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('riaapp', '0004_auto_20190909_1547'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strength', models.IntegerField(default=1)),
                ('indirect', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='DepType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('directional', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='NLPDoc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc', models.BinaryField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Req',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=2000)),
                ('indeg', models.IntegerField(default=-1)),
                ('outdeg', models.IntegerField(default=-1)),
                ('nlp_doc', models.ForeignKey(default=-1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='riaapp.NLPDoc')),
            ],
        ),
        migrations.CreateModel(
            name='Path',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('deps', models.ManyToManyField(related_name='_path_deps_+', to='riaapp.Dep')),
            ],
        ),
        migrations.CreateModel(
            name='DepLearnInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('positive', models.BooleanField(default=True)),
                ('dep', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='riaapp.Dep')),
            ],
        ),
        migrations.AddField(
            model_name='dep',
            name='dep_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='riaapp.DepType'),
        ),
        migrations.AddField(
            model_name='dep',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='riaapp.Req'),
        ),
        migrations.AddField(
            model_name='dep',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='riaapp.Req'),
        ),
    ]
