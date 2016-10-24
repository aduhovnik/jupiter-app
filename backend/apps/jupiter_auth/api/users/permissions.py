# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from core.api.generic.permissions import ViewPermission


class UserViewPermission(ViewPermission):

    perm = 'jupiter_auth.manage_himself'

    def has_permission(self, request, view):
        username = view.kwargs.get('username')
        if username == request.user.username and request.user.has_perm(self.perm):
            return True
        return super(UserViewPermission, self).has_permission(request, view)
