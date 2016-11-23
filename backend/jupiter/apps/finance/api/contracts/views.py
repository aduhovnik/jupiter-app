# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from core.api.generic.views import ReadOnlyModelViewSet
from jupiter_auth.authentication import TokenAuthentication
import finance.api.contracts.serializers as serializers
import finance.models as fin_models


class ContractView(ReadOnlyModelViewSet):
    queryset = fin_models.Contract.objects.all()
    serializer_class = serializers.ContractSerializer

    authentication_classes = (TokenAuthentication,)
