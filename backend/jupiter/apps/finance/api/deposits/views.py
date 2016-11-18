# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from core.api.generic.views import ReadOnlyModelViewSet
from jupiter_auth.api.users.permissions import ManageSelfPermission
from jupiter_auth.authentication import TokenAuthentication
import finance.api.deposits.serializers as serializers
import finance.models as fin_models


class DepositView(ReadOnlyModelViewSet):
    queryset = fin_models.Deposit.objects.all()
    serializer_class = serializers.DepositSerializer

    authentication_classes = (TokenAuthentication,)


class DepositTemplateView(ReadOnlyModelViewSet):
    queryset = fin_models.DepositTemplate.objects.all()
    serializer_class = serializers.DepositTemplateSerializer