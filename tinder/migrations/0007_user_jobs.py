# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-09 03:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinder', '0006_auto_20161009_0347'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='jobs',
            field=models.CharField(default='', max_length=200),
        ),
    ]
