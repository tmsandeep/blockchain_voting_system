# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-06 17:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0018_auto_20170406_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voterchoice',
            name='voter_address',
            field=models.CharField(choices=[('mpMtRQUB9XeyXiJevZL6TuLxbvNJJys74j', 'Voter1Address'), ('miyLyx2bp4buCnRV4y93RKNH3Lp1s89zQa', 'voter2Address'), ('n39HtcDLnXrxNH4yEra8K7QfVKLN2CJ3Sk', 'voter3Address')], max_length=36),
        ),
        migrations.AlterField(
            model_name='voterslistchoice',
            name='voters',
            field=models.CharField(choices=[('mpMtRQUB9XeyXiJevZL6TuLxbvNJJys74j', 'Voter1Address'), ('miyLyx2bp4buCnRV4y93RKNH3Lp1s89zQa', 'voter2Address'), ('n39HtcDLnXrxNH4yEra8K7QfVKLN2CJ3Sk', 'voter3Address')], max_length=36),
        ),
    ]
