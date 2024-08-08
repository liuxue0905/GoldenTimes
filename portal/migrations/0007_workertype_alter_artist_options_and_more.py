# Generated by Django 5.0.7 on 2024-08-07 07:26

import django.db.models.deletion
import portal.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_auto_20180628_0105'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkerType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': '参与者类型',
                'verbose_name_plural': '参与者类型',
                'db_table': 'worker_type',
            },
        ),
        migrations.AlterModelOptions(
            name='artist',
            options={'ordering': ['name'], 'verbose_name': '艺人', 'verbose_name_plural': '艺人'},
        ),
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ['name'], 'verbose_name': '唱片公司', 'verbose_name_plural': '唱片公司'},
        ),
        migrations.AlterModelOptions(
            name='logimportartist',
            options={'ordering': ['-datetime_start'], 'verbose_name': '导入 艺人', 'verbose_name_plural': '导入 艺人'},
        ),
        migrations.AlterModelOptions(
            name='logimportrecord',
            options={'ordering': ['-datetime_start'], 'verbose_name': '导入 唱片', 'verbose_name_plural': '导入 唱片'},
        ),
        migrations.AlterModelOptions(
            name='record',
            options={'ordering': ['year', 'release_order', 'title'], 'verbose_name': '唱片', 'verbose_name_plural': '唱片'},
        ),
        migrations.AlterModelOptions(
            name='song',
            options={'ordering': ['track'], 'verbose_name': '歌曲', 'verbose_name_plural': '歌曲列表'},
        ),
        migrations.AlterField(
            model_name='artist',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='artistavatar',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='artistavatar',
            name='image',
            field=portal.models.TryExceptImageField(height_field='height', null=True, storage=portal.models.FileStorage(), upload_to=portal.models.artist_avatar_upload_to, verbose_name='图片', width_field='width'),
        ),
        migrations.AlterField(
            model_name='artistimages',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='artistimages',
            name='image',
            field=portal.models.TryExceptImageField(height_field='height', null=True, storage=portal.models.FileStorage(), upload_to=portal.models.artist_images_upload_to, verbose_name='图片', width_field='width'),
        ),
        migrations.AlterField(
            model_name='company',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='logimportartist',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='logimportrecord',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='record',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='recordcover',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='recordcover',
            name='image',
            field=portal.models.TryExceptImageField(height_field='height', null=True, storage=portal.models.FileStorage(), upload_to=portal.models.record_cover_upload_to, verbose_name='图片', width_field='width'),
        ),
        migrations.AlterField(
            model_name='recordimages',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='recordimages',
            name='image',
            field=portal.models.TryExceptImageField(height_field='height', null=True, storage=portal.models.FileStorage(), upload_to=portal.models.record_images_upload_to, verbose_name='图片', width_field='width'),
        ),
        migrations.AlterField(
            model_name='song',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='SongWorker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='名称')),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('order', models.IntegerField(verbose_name='排序')),
                ('song', models.ForeignKey(db_column='song_id', on_delete=django.db.models.deletion.CASCADE, to='portal.song')),
                ('type', models.ForeignKey(blank=True, db_column='type', null=True, on_delete=django.db.models.deletion.SET_NULL, to='portal.workertype', verbose_name='类型')),
            ],
            options={
                'verbose_name': '歌曲参与者',
                'verbose_name_plural': '歌曲参与者',
                'db_table': 'song_worker',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='RecordWorker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='名称')),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('order', models.IntegerField(verbose_name='排序')),
                ('record', models.ForeignKey(db_column='record_id', on_delete=django.db.models.deletion.CASCADE, to='portal.record')),
                ('type', models.ForeignKey(blank=True, db_column='type', null=True, on_delete=django.db.models.deletion.SET_NULL, to='portal.workertype', verbose_name='类型')),
            ],
            options={
                'verbose_name': '唱片参与者',
                'verbose_name_plural': '唱片参与者',
                'db_table': 'record_worker',
                'ordering': ['order'],
            },
        ),
    ]