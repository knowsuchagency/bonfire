# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-07 02:31
from __future__ import unicode_literals

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
                ('bio', models.TextField(blank=True)),
                ('schools', models.CharField(blank=True, max_length=50)),
                ('jobs', models.CharField(blank=True, max_length=50)),
                ('instagram_username', models.CharField(blank=True, max_length=30)),
                ('mentions_snapchat', models.BooleanField(default=False)),
                ('mentions_kik', models.BooleanField(default=False)),
                ('mentions_instagram', models.BooleanField(default=False)),
            ],
        ),
    ]
