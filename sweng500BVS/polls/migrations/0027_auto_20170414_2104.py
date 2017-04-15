# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-15 02:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0026_auto_20170414_2103'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoteTxList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txId', models.CharField(max_length=366)),
                ('voter_address', models.CharField(choices=[('mpMtRQUB9XeyXiJevZL6TuLxbvNJJys74j', 'Voter1Address'), ('miyLyx2bp4buCnRV4y93RKNH3Lp1s89zQa', 'Voter2Address'), ('n39HtcDLnXrxNH4yEra8K7QfVKLN2CJ3Sk', 'Voter3Address')], max_length=36)),
                ('contestant_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listTx', related_query_name='listTx', to='polls.ContestantChoice')),
            ],
        ),
        migrations.RemoveField(
            model_name='voterchoice',
            name='voting_complete',
        ),
    ]