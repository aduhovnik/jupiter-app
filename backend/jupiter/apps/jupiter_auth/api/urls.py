# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from jupiter_auth.api.auth.views import SignInView, SignOutView, SignUpView
from jupiter_auth.api.users.views import UserView


router = DefaultRouter()
router.register('users', UserView, base_name='user-profiles')
router.register('sign-in', SignInView, base_name='sign-in')
router.register('sign-out', SignOutView, base_name='sign-out')
router.register('sign-up', SignUpView, base_name='sign-up')


urlpatterns = [
    url(r'^api/', include(router.urls))
]