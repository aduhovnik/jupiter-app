# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-23 17:02
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0013_auto_20161123_1654'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deposittemplate',
            old_name='defeasans',
            new_name='closing',
        ),
        migrations.AlterField(
            model_name='credittemplate',
            name='allowed_methods_of_ensuring',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(choices=[(0, 'Fine'), (1, 'Plegde'), (2, 'Surety')]), size=None),
        ),
    ]
