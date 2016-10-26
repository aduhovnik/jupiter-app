# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models
from django.conf import settings


class UserProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    identification_number = models.CharField(max_length=30)
    passport_number = models.CharField(max_length=20)
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=200)
    age = models.IntegerField()
    passport_expires = models.DateField()
    birth_date = models.DateField()
    family_status = models.TextField()
    dependants = models.TextField()
    income = models.TextField()
    realty = models.TextField()
    job = models.TextField()

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'
        permissions = (
            ('view_user', 'Can view users'),
            ('manage_himself', 'Can manage himself'),
        )
