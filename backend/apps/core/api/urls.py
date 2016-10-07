# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from .users.views import UserView
from .groups.views import GroupView


router = DefaultRouter()
router.register('users/groups', GroupView, 'user-groups')
router.register('users', UserView, 'users')


urlpatterns = [
    url('^api/', include(router.urls))
]
