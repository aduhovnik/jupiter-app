# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import finance.api.contracts.serializers as serializers
import finance.models as fin_models
from core.api.generic.views import ModelViewSet
from jupiter_auth.authentication import TokenAuthentication


class ContractView(ModelViewSet):
    queryset = fin_models.Contract.objects.all()
    serializer_class = serializers.ContractSerializer

    authentication_classes = (TokenAuthentication,)
