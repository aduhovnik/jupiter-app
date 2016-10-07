# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import Group
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import GroupSerializer


class GroupView(ReadOnlyModelViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
