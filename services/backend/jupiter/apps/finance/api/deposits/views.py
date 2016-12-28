# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

import finance.models as fin_models
import finance.api.deposits.serializers as serializers
from jupiter_auth.authentication import TokenAuthentication
from core.api.generic.views import ModelViewSet, ReadOnlyModelViewSet
from jupiter_auth.utils import get_or_create_clients_group, get_or_create_admins_group


class DepositView(ModelViewSet):
    queryset = fin_models.Deposit.objects.all()
    serializer_class = serializers.DepositSerializer

    def get_queryset(self):
        queryset = super(DepositView, self).get_queryset()
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
            "template_id": id
            "amount": money_amount, in BYN
            "duration": duration,
            "percentage": percentage (0...100),
            "currency": currency,
            "account_id": source_account_id,
        }
        admin can confirm it
        """
        money_amount = request.data['amount']
        client = request.user
        template = fin_models.DepositTemplate.objects.get(pk=request.data['template_id'])
        duration = request.data['duration']
        percentage = request.data['percentage']
        currency = request.data['currency']
        account_id = request.data['account_id']
        if not fin_models.Account.objects.filter(pk=account_id):
            return Response('Указанного счета не существует.', status=status.HTTP_400_BAD_REQUEST)
        account = fin_models.Account.objects.get(pk=account_id)
        if account.status in fin_models.Account.INOPERABLE_STATUSES:
            return Response('Операции с указанным счетом невозможны.', status=status.HTTP_400_BAD_REQUEST)
        deposit = fin_models.Deposit.create(client, template, money_amount, duration,
                                            percentage, currency, account_id)
        if deposit is None:
            return Response('На указаном счете недостаточно денег', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Заявка подана. Указанный счет временно заморожен.', status=status.HTTP_200_OK)

    @detail_route(methods=['PATCH'])
    def confirm_create_claim(self, request, *args, **kwargs):
        deposit = self.get_object()
        if deposit.status != deposit.STATUS_REQUESTED_CREATING:
            return Response('Заявка на создание депозита уже была обработана.', status=status.HTTP_400_BAD_REQUEST)
        else:
            if deposit.confirm():
                return Response('Создание депозита подтверждено', status=status.HTTP_200_OK)
            else:
                return Response('Отклонено банком.', status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['PATCH'])
    def reject_create_claim(self, request, *args, **kwargs):
        """
        :param request:
        {
            "cause", cause of rejection
        }
        """
        deposit = self.get_object()
        cause = request.data['cause']
        if deposit.status != deposit.STATUS_REQUESTED_CREATING:
            return Response('Заявка на создание депозита уже была обработана.', status=status.HTTP_400_BAD_REQUEST)
        else:
            deposit.reject(cause)
            return Response('Создание депозита отклонено', status=status.HTTP_200_OK)

    @detail_route(methods=['PATCH'])
    def leave_close_claim(self, request, *args, **kwargs):
        """
        :param request:
        {
            "target_account_id": account_id
        }
        """
        deposit = self.get_object()
        if deposit.status in deposit.INOPERABLE_STATUSES:
            return Response('Операции с депозитом невозможны', status=status.HTTP_400_BAD_REQUEST)
        if deposit.status == deposit.STATUS_REQUESTED_CLOSING:
            return Response('Заявка на закрытие депозита уже подана.', status=status.HTTP_400_BAD_REQUEST)
        target_account_id = request.data['target_account_id']
        if not fin_models.Account.objects.filter(pk=target_account_id):
            return Response('Указанного счета не существует.', status=status.HTTP_400_BAD_REQUEST)
        account = fin_models.Account.objects.get(pk=target_account_id)
        if account.status in fin_models.Account.INOPERABLE_STATUSES:
            return Response('Операции с указанным счетом невозможны.', status=status.HTTP_400_BAD_REQUEST)
        res, info = deposit.leave_close_claim(target_account_id)
        return Response(info, status=status.HTTP_200_OK if res else status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['PATCH'])
    def confirm_close_claim(self, request, *args, **kwargs):
        deposit = self.get_object()
        if deposit.status != deposit.STATUS_REQUESTED_CLOSING:
            return Response('Заявка на закрытие депозита не подана.', status=status.HTTP_400_BAD_REQUEST)
        if deposit.close_confirm():
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
        deposit = self.get_object()
        if deposit.status != deposit.STATUS_REQUESTED_CLOSING:
            return Response('Заявка на закрытие депозита не подана.', status=status.HTTP_400_BAD_REQUEST)
        cause = request.data['cause']
        if deposit.close_reject(cause):
            return Response('Закрытие отклонено.', status=status.HTTP_200_OK)
        else:
            return Response('Заявка на закрытие не была подана.', status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['POST'])
    def put_money(self, request, *args, **kwargs):
        """
        :param request:
        {
            "amount": money_amount (in BLR - only in BLR),
            "account_id": account_id (get money from account)
        Add money to deposit
        """
        deposit = self.get_object()
        if deposit.status != deposit.STATUS_ACTIVE:
            return Response('Операции с депозитом невозможны', status=status.HTTP_400_BAD_REQUEST)
        if not deposit.additional_contributions:
            return Response('Данный депозит не позволяет дополнительных начислений.')
        amount = request.data['amount']
        account_id = request.data["account_id"]
        if not fin_models.Account.objects.filter(pk=account_id):
            return Response('Указанного счета не существует.', status-status.HTTP_400_BAD_REQUEST)
        account = fin_models.Account.objects.get(pk=account_id)
        if request.user != account.client:
            return Response('Невозможно использование чужого счета.', status.HTTP_400_BAD_REQUEST)
        if account.status in fin_models.Account.INOPERABLE_STATUSES:
            return Response('Операции с указанным счетом невозможны.', status=status.HTTP_400_BAD_REQUEST)
        if account.get_money(amount):
            if deposit.additional_contribution(amount):
                deposit.save()
                return Response('Дополнительные средства перечислены.', status=status.HTTP_200_OK)
            else:
                account.put_money(amount)
                return Response('Отклонено банком. Ваш счет не подтвержден или не активен.',
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Недостаточно средств на счете', status=status.HTTP_400_BAD_REQUEST)


class DepositTemplateView(ReadOnlyModelViewSet):
    queryset = fin_models.DepositTemplate.objects.all()
    serializer_class = serializers.DepositTemplateSerializer
