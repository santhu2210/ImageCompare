# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-08 13:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_server', '0003_auto_20180508_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageupload',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='orgImages/%Y/%m/%d'),
        ),
    ]
