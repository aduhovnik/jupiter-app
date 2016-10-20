# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User
from core.api.users.serializers import UserSerializer
from core.api.generic.views import ReadOnlyModelViewSet


class UserView(ReadOnlyModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
