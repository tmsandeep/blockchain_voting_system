# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-31 13:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20170331_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ballot',
            name='ballot_address',
            field=models.CharField(choices=[('mh4w5JnU662ddHywJU3X1wYL6mufjd6Egz', 'ballot1Address')], max_length=36),
        ),
        migrations.AlterField(
            model_name='choice',
            name='voter_address',
            field=models.CharField(choices=[('mpMtRQUB9XeyXiJevZL6TuLxbvNJJys74j', 'Voter1Address'), ('miyLyx2bp4buCnRV4y93RKNH3Lp1s89zQa', 'voter2Address'), ('n39HtcDLnXrxNH4yEra8K7QfVKLN2CJ3Sk', 'voter3Address')], max_length=36),
        ),
    ]