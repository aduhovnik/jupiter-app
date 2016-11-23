# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from core.api.generic.views import ReadOnlyModelViewSet
from jupiter_auth.authentication import TokenAuthentication
import finance.api.accounts.serializers as serializers
import finance.models as fin_models


class AccountView(ReadOnlyModelViewSet):
    queryset = fin_models.Account.objects.all()
    serializer_class = serializers.AccountSerializer

    authentication_classes = (TokenAuthentication,)
