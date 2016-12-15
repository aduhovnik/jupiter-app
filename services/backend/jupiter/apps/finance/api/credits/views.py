# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import finance.api.credits.serializers as serializers
import finance.models as fin_models
from core.api.generic.views import ModelViewSet
from jupiter_auth.authentication import TokenAuthentication


class CreditView(ModelViewSet):
    queryset = fin_models.Credit.objects.all()
    serializer_class = serializers.CreditSerializer

    authentication_classes = (TokenAuthentication,)


class CreditTemplateView(ModelViewSet):
    queryset = fin_models.CreditTemplate.objects.all()
    serializer_class = serializers.CreditTemplateSerializer
