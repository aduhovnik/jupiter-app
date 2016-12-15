# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import finance.api.transactions.serializers as serializers
import finance.models as fin_models
from core.api.generic.views import ModelViewSet
from jupiter_auth.authentication import TokenAuthentication


class TransactionView(ModelViewSet):
    serializer_class = serializers.TransactionSerializer
    queryset = fin_models.Transaction.objects.all()

    authentication_classes = (TokenAuthentication,)
