# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth import get_user_model
from core.api.generic.views import ReadOnlyModelViewSet
from jupiter_auth.api.users.permissions import UserViewPermission
from jupiter_auth.authentication import TokenAuthentication
from jupiter_auth.api.users.serializers import UserSerializer


class UserView(ReadOnlyModelViewSet):

    lookup_field = 'username'
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (UserViewPermission,)
