# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from core.api.generic.utils import prettify_response
from jupiter_auth.factories import UserFactory
from jupiter_auth.utils import get_or_create_default_group


class UserTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(groups=[get_or_create_default_group()])

    def test_client_can_view_himself(self):
        self.client.force_authenticate(self.user)

        url = reverse('users-detail', args=(self.user.username,))
        r = self.client.get(url)
        self.assertEqual(
            r.status_code,
            status.HTTP_200_OK,
            prettify_response('User can view his profile', r)
        )
