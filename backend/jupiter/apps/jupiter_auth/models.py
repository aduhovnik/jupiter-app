# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        permissions = (
            ('view_user', 'Can view users'),
            ('manage_himself', 'Can manage himself'),
        )


class UserProfile(models.Model):

    user = models.OneToOneField(User, related_name='profile')
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
