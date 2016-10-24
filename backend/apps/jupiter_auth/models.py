# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models
from django.conf import settings


class UserProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    age = models.IntegerField(null=True)

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'
        permissions = (
            ('view_user', 'Can view users'),
            ('manage_himself', 'Can manage himself'),
        )
