# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-01 01:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20170331_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='ballot',
            name='isItVoter',
            field=models.BooleanField(default=False),
        ),
    ]
