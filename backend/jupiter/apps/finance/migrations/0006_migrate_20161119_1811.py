# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0005_auto_20161119_1438'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deposittemplate',
            name='percentage',
        ),
        migrations.RemoveField(
            model_name='credittemplate',
            name='percentage',
        ),
        migrations.AddField(
            model_name='credittemplate',
            name='percentage',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
        migrations.AddField(
            model_name='deposittemplate',
            name='percentage',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
         migrations.RemoveField(
            model_name='credittemplate',
            name='max_amount',
        ),
        migrations.RemoveField(
            model_name='credittemplate',
            name='min_amount',
        ),
        migrations.AddField(
            model_name='credittemplate',
            name='max_amount',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
        migrations.AddField(
            model_name='credittemplate',
            name='min_amount',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
    ]
