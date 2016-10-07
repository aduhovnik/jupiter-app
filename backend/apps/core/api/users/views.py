# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import UserSerializer


class UserView(ReadOnlyModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
