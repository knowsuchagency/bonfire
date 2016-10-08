# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-08 08:26
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('age', models.IntegerField()),
                ('bio', models.TextField(default='')),
                ('schools', models.CharField(blank=True, max_length=100)),
                ('jobs', models.CharField(blank=True, max_length=100)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('distance', models.FloatField(default=0.0)),
                ('instagram_username', models.CharField(default='None', max_length=30)),
                ('mentions_snapchat', models.BooleanField(default=False)),
                ('mentions_kik', models.BooleanField(default=False)),
                ('mentions_instagram', models.BooleanField(default=False)),
                ('liked', models.BooleanField(default=False)),
                ('from_other', models.BooleanField(default=False)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('tinder_id', models.CharField(max_length=25)),
            ],
        ),
    ]
