# Generated by Django 2.0.6 on 2018-06-27 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_auto_20180621_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='release_detail',
            field=models.CharField(blank=True, help_text='空|yyyy|yyyymm|yyyymmdd', max_length=8, null=True, verbose_name='发布时间'),
        ),
        migrations.AlterField(
            model_name='record',
            name='release',
            field=models.CharField(blank=True, help_text='yyyy', max_length=4, null=True, verbose_name='年代'),
        ),
        migrations.AlterField(
            model_name='record',
            name='release_order',
            field=models.CharField(blank=True, help_text='yyyy0000', max_length=128, null=True, verbose_name='发布时间排序'),
        ),
    ]
