# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import finance.api.accounts.serializers as serializers
import finance.models as fin_models
from core.api.generic.views import ModelViewSet
from jupiter_auth.authentication import TokenAuthentication


class AccountView(ModelViewSet):
    queryset = fin_models.Account.objects.all()
    serializer_class = serializers.AccountSerializer

    authentication_classes = (TokenAuthentication,)
