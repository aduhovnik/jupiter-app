# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from django.db import models
from djmoney.models.fields import MoneyField
from finance.settings import DEPOSIT_TEMPLATES, CREDIT_TEMPLATES
from finance.models import DepositTemplate, CreditTemplate

logger = logging.getLogger('jupiter')

def init_deposit_templates():
    DepositTemplate.objects.exclude(name__in=[d['name'] for d in DEPOSIT_TEMPLATES]).delete()
    for template_data in DEPOSIT_TEMPLATES:
        defaults = {k:template_data[k] for k in template_data.keys()}
        del defaults['name']
        deposite_template, created = DepositTemplate.objects.update_or_create(name=template_data['name'], defaults=defaults)
        logger.info('Initialized deposit template "{}"'.format(template_data['name']))

def init_credit_templates():
    CreditTemplate.objects.exclude(name__in=[d['name'] for d in CREDIT_TEMPLATES]).delete()
    for template_data in CREDIT_TEMPLATES:
        defaults = {k:template_data[k] for k in template_data.keys()}
        del defaults['name']
        credit_template, created = CreditTemplate.objects.update_or_create(name=template_data['name'], defaults=defaults)
        logger.info('Initialized credit template "{}"'.format(template_data['name']))
