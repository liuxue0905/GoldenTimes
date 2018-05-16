# Generated by Django 2.0.2 on 2018-05-16 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogImportArtist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_start', models.DateTimeField(null=True)),
                ('datetime_end', models.DateTimeField(null=True)),
                ('status', models.IntegerField(blank=True, choices=[(0, '开始'), (1, '成功'), (-1, '失败')], null=True)),
                ('file_excel', models.FileField(null=True, upload_to='')),
                ('file_log', models.FileField(null=True, upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-datetime_start'],
            },
        ),
        migrations.CreateModel(
            name='LogImportRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_start', models.DateTimeField(null=True)),
                ('datetime_end', models.DateTimeField(null=True)),
                ('status', models.IntegerField(blank=True, choices=[(0, '开始'), (1, '成功'), (-1, '失败')], null=True)),
                ('file_excel', models.FileField(null=True, upload_to='')),
                ('file_log', models.FileField(null=True, upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-datetime_start'],
            },
        ),
        migrations.DeleteModel(
            name='ExcelLog',
        ),
    ]
