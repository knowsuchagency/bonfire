# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-09 04:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinder', '0007_user_jobs'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='liked_date',
            field=models.DateField(auto_now=True),
        ),
    ]