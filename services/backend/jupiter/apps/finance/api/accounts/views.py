# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework import status

import finance.api.accounts.serializers as serializers
import finance.models as fin_models
from core.api.generic.views import ModelViewSet
from jupiter_auth.authentication import TokenAuthentication
from jupiter_auth.utils import get_or_create_clients_group, get_or_create_admins_group


class AccountView(ModelViewSet):
    queryset = fin_models.Account.objects.all()
    serializer_class = serializers.AccountSerializer

    def get_queryset(self):
        queryset = super(AccountView, self).get_queryset()
        if self.request.user.is_superuser:
            return queryset
        if get_or_create_admins_group() in self.request.user.groups.all():
            return queryset
        elif get_or_create_clients_group() in self.request.user.groups.all():
            return queryset.filter(client=self.request.user)
        else:
            return queryset.none()

    @list_route(methods=['POST'])
    def leave_create_claim(self, request, *args, **kwargs):
        """
        :param request:
        {
            "amount": money_amount, in BYN
        }
        dummy - money from the wind
        admin can confirm it
        """
        first_contribution = request.data['amount']
        client = request.user
        fin_models.Account.create(False, client, first_contribution)
        return Response('Заявка подана', status=status.HTTP_200_OK)

    @detail_route(methods=['PATCH'])
    def confirm_create_claim(self, request, *args, **kwargs):
        account = self.get_object()
        if account.status != fin_models.Account.STATUS_ACTIVE:
            return Response('Операции со счетом невозможны', status=status.HTTP_400_BAD_REQUEST)
        elif account.is_active:
            return Response('Счет уже создан', status=status.HTTP_400_BAD_REQUEST)
        else:
            if account.confirm():
                return Response('Создание счета подтверждено', status=status.HTTP_200_OK)
            return Response('Создание счета отклонено банком', status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['PATCH'])
    def reject_create_claim(self, request, *args, **kwargs):
        """
        :param request:
        {
            "cause", cause of rejection
        }
        """
        account = self.get_object()
        cause = request.data['cause']
        if account.status != fin_models.Account.STATUS_ACTIVE:
            return Response('Операции со счетом невозможны', status=status.HTTP_400_BAD_REQUEST)
        elif account.is_active:
            return Response('Счет уже создан', status=status.HTTP_400_BAD_REQUEST)
        else:
            account.reject(cause)
            return Response('Создание счета отклонено', status=status.HTTP_200_OK)

    @detail_route(methods=['PATCH'])
    def leave_close_claim(self, request, *args, **kwargs):
        """
        :param request:
        {
            "target_account_id": account_id
        }
        """
        account = self.get_object()
        target_account_id = request.data['target_account_id']
        if account.leave_close_claim(target_account_id):
            return Response('Заявка на закрытие отправлена.', status=status.HTTP_200_OK)
        else:
            return Response('Счет не может быть закрыт.', status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['PATCH'])
    def confirm_close_claim(self, request, *args, **kwargs):
        account = self.get_object()
        if account.close_confirm():
            return Response('Закрытие подтверждено, деньги переведены.', status=status.HTTP_200_OK)
        else:
            return Response('Заявка на закрытие не была подана.', status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['PATCH'])
    def reject_close_claim(self, request, *args, **kwargs):
        """
        :param request:
        {
            "cause", cause of rejection
        }
        """
        account = self.get_object()
        cause = request.data['cause']
        if account.close_reject(cause):
            return Response('Закрытие отклонено.', status=status.HTTP_200_OK)
        else:
            return Response('Заявка на закрытие не была подана.', status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def assign(self, request, *args, **kwargs):
        """
        :param request:
        {
            'account_number': 13digits
        }
        """
        client = request.user
        account_number = request.data['account_number']
        res, info = fin_models.Account.assign(client, account_number)
        return Response(info, status=status.HTTP_200_OK if res else status.HTTP_400_BAD_REQUEST)
