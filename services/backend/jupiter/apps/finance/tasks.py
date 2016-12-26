# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from .models import Credit, Deposit

# TODO: schedule to execute every day
# TODO: mb use https://github.com/tivix/django-cron


def daily_tasks():
    update_credits()
    update_deposits()


def update_credits():
    objects = Credit.objects.exclude(status__in=Credit.INOPERABLE_STATUSES)
    for credit in objects:
        credit.daily_update()


def update_deposits():
    objects = Deposit.objects.exclude(status__in=Deposit.INOPERABLE_STATUSES)
    for deposit in objects:
        deposit.daily_update()
