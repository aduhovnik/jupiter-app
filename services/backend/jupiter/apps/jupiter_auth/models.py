# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models

from finance.utils import money_field


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
    address = models.CharField(max_length=300, null=True)
    phone = models.CharField(max_length=200, null=True)
    age = models.IntegerField(null=True)
    passport_expires = models.DateField(null=True)
    birth_date = models.DateField(null=True)
    family_status = models.TextField(null=True)
    dependants = models.IntegerField(null=True)
    income = money_field(null=True)
    realty = models.TextField(null=True)
    job = models.TextField(null=True)
    number_of_times_90_more_days_late = models.IntegerField(default=0)
    number_of_times_30_59_days_late = models.IntegerField(default=0)
    number_of_times_60_89_days_late = models.IntegerField(default=0)

    def treat_days_late(self, days_late):
        if 30 <= days_late < 60:
            self.number_of_times_30_59_days_late += 1
        elif 60 <= days_late < 90:
            self.number_of_times_60_89_days_late += 1
        elif 90 <= days_late:
            self.number_of_times_90_more_days_late += 1
        self.save()

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'
