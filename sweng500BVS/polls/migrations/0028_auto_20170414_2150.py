# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-15 02:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0027_auto_20170414_2104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='votetxlist',
            name='contestant_address',
        ),
        migrations.AddField(
            model_name='voterchoice',
            name='sendHex',
            field=models.CharField(default='None', max_length=366),
        ),
        migrations.DeleteModel(
            name='VoteTxList',
        ),
    ]