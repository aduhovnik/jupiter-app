# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand
from jupiter_auth.settings import GROUPS


class Command(BaseCommand):

    logger = logging.getLogger('jupiter')

    def handle(self, *args, **kwargs):
        self.logger.info('Initializing groups...')
        Group.objects.exclude(name__in=[g['name'] for g in GROUPS]).delete()
        for group_data in GROUPS:
            perms = Permission.objects.filter(codename__in=group_data['permissions'])
            group, created = Group.objects.get_or_create(name=group_data['name'])
            group.permissions.clear()
            group.permissions.add(*perms)
            self.logger.info('Initialized group "{}"'.format(group_data['name']))
        self.logger.info('Initializing groups complete')
