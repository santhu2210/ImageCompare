# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-06-05 10:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_server', '0011_userlogin_userpasswordtoken'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='campaign',
            options={'verbose_name_plural': 'Campaign'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'category'},
        ),
        migrations.AddField(
            model_name='campaign',
            name='formData',
            field=models.TextField(blank=True, null=True),
        ),
    ]
