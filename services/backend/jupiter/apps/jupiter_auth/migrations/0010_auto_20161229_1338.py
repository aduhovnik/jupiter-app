# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 13:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jupiter_auth', '0009_auto_20161229_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='identification_number',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='passport_number',
            field=models.CharField(max_length=20),
        ),
    ]