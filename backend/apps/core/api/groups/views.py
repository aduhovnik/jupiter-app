# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import Group
from core.api.groups.serializers import GroupSerializer
from core.api.generic.views import ReadOnlyModelViewSet


class GroupView(ReadOnlyModelViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
