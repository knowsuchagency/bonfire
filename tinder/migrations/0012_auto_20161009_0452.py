# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-09 04:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tinder', '0011_auto_20161009_0452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='liked_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
