# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth import get_user_model
from core.api.generic.views import ReadOnlyModelViewSet
from jupiter_auth.api.users.permissions import ManageSelfPermission
from jupiter_auth.authentication import TokenAuthentication
from jupiter_auth.api.users.serializers import UserSerializer


class UserView(ReadOnlyModelViewSet):

    lookup_field = 'username'
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (ManageSelfPermission,)

    def retrieve(self, request, *args, **kwargs):
        if self.kwargs[self.lookup_field] == 'me':
            self.kwargs[self.lookup_field] = getattr(self.request.user, self.lookup_field)
        return super(UserView, self).retrieve(request, *args, **kwargs)
