# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import finance.api.contracts.serializers as serializers
import finance.models as fin_models
from core.api.generic.views import ModelViewSet
from jupiter_auth.authentication import TokenAuthentication
from jupiter_auth.utils import get_or_create_clients_group, get_or_create_admins_group


class ContractView(ModelViewSet):
    queryset = fin_models.Contract.objects.all()
    serializer_class = serializers.ContractSerializer

    def get_queryset(self):
        queryset = super(ContractView, self).get_queryset()
        if self.request.user.is_superuser:
            return queryset
        if get_or_create_admins_group() in self.request.user.groups.all():
            return queryset
        elif get_or_create_clients_group() in self.request.user.groups.all():
            return queryset.filter(client=self.request.user)
        else:
            return queryset.none()
