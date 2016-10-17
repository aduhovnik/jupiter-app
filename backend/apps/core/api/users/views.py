# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User
from .serializers import UserSerializer
from ..generic.views import ReadOnlyModelViewSet


class UserView(ReadOnlyModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
