# Generated by Django 2.0.2 on 2018-06-21 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_auto_20180529_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='release',
            field=models.CharField(blank=True, help_text='yyyy|yyyymm|yyyymmdd', max_length=8, null=True, verbose_name='发布时间'),
        ),
    ]
