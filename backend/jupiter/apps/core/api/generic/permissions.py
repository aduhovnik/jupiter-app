# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import Permission
from rest_framework.permissions import BasePermission


class ViewPermission(BasePermission):

    def has_permission(self, request, view):
        model = view.queryset and view.queryset.model
        if model:
            try:
                perm = Permission.objects.get(codename__iexact='view_{}'.format(model.__name__))
                return request.user.has_perm(perm.name)
            except Permission.DoesNotExist:
                pass
        return True
