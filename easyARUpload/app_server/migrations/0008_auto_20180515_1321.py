# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-15 13:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_server', '0007_auto_20180515_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
