# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from core.api.generic.tests import ReadOnlyModelTestMixin
from jupiter_auth.factories import UserFactory


class UserTestCase(ReadOnlyModelTestMixin, APITestCase):

    base_name = 'users'
    factory_class = UserFactory
    lookup_field = 'username'

    def test_client_can_view_himself(self):
        url = reverse('users-detail', args=("me",))
        perm = Permission.objects.get(codename='manage_himself')
        self.check_permission(perm, url, 'get')
