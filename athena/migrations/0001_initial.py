# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-29 18:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EHR_times',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('times', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='RTLS_times',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interaction_id', models.IntegerField(default=0)),
                ('times', models.CharField(max_length=200)),
            ],
        ),
    ]
