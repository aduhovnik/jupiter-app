# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import finance.api.deposits.serializers as serializers
import finance.models as fin_models
from core.api.generic.views import ModelViewSet
from jupiter_auth.authentication import TokenAuthentication


class DepositView(ModelViewSet):
    queryset = fin_models.Deposit.objects.all()
    serializer_class = serializers.DepositSerializer

    authentication_classes = (TokenAuthentication,)


class DepositTemplateView(ModelViewSet):
    queryset = fin_models.DepositTemplate.objects.all()
    serializer_class = serializers.DepositTemplateSerializer
