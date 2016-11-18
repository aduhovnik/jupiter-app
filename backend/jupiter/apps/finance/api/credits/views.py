# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from core.api.generic.views import ReadOnlyModelViewSet
from jupiter_auth.api.users.permissions import ManageSelfPermission
from jupiter_auth.authentication import TokenAuthentication
import finance.api.credits.serializers as serializers
import finance.models as fin_models


class CreditView(ReadOnlyModelViewSet):
    queryset = fin_models.Credit.objects.all()
    serializer_class = serializers.CreditSerializer

    authentication_classes = (TokenAuthentication,)


class CreditTemplateView(ReadOnlyModelViewSet):
    queryset = fin_models.CreditTemplate.objects.all()
    serializer_class = serializers.CreditTemplateSerializer