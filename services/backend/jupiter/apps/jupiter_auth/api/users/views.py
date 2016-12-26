# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
from os import environ
from urllib2 import Request, urlopen

from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ValidationError
from core.utils import send_mail
from core.api.generic.views import ModelViewSet
from finance.models import Credit, Deposit, Transaction
from jupiter_auth.utils import get_or_create_clients_group, get_or_create_admins_group
from jupiter_auth.api.users.permissions import ManageSelfPermission
from jupiter_auth.api.users.serializers import UserSerializer


class UserView(ModelViewSet):

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (ManageSelfPermission,)

    def get_queryset(self):
        queryset = super(UserView, self).get_queryset()
        if self.request.user.is_superuser:
            return queryset
        elif self.kwargs.get(self.lookup_field) == 'me':
            return queryset.filter(pk=self.request.user.pk)
        elif get_or_create_admins_group() in self.request.user.groups.all():
            return queryset.filter(groups=get_or_create_clients_group())
        else:
            return queryset.none()

    def get_object(self):
        if self.kwargs[self.lookup_field] == 'me':
            return self.request.user
        else:
            return super(UserView, self).get_object()

    @detail_route(methods=['GET'])
    def activate(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_active:
            raise ValidationError('Пользователь уже активирован')

        user.is_active = True
        user.save()

        message = render_to_string('auth/account_confirm_email.html')
        try:
            send_mail('no-reply@jupiter-group.com', user.email, 'Ваш аккаунт подтвержден', message)
        except Exception as e:
            raise ValidationError('Ошибка при отправке письма: {}'.format(e))
        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=['GET'])
    def deactivate(self, request, *args, **kwargs):
        user = self.get_object()
        if not user.is_active:
            raise ValidationError('Пользователь уже деактивирован')

        user.is_active = False
        user.save()

        message = render_to_string('auth/account_deactivate_email.html')
        try:
            send_mail('no-reply@jupiter-group.com', user.email, 'Ваш аккаунт отключен', message)
        except Exception as e:
            raise ValidationError('Ошибка при отправке письма: {}'.format(e))
        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=['GET'])
    def scoring(self, request, *args, **kwargs):
        client = self.get_object()
        client_credits = Credit.objects.filter(client=client)

        scoring_data = {
            "age":
                client.profile.age,
            "credit_monthly_payments":[
                float(value)
                for value in client_credits.values_list('minimum_monthly_pay', flat=True)
                if value > 0
            ],
            "credits_residue": [
                float(value)
                for value in client_credits.values_list('residue', flat=True)
                if value > 0
            ],
            "credit_limits": [
                float(value)
                for value in client_credits.values_list('total_sum', flat=True)
                if value > 0
            ],
            "MonthlyIncome":
                float(client.profile.income.amount),
            "NumberOfDependents":
                client.profile.dependants,
            "NumberOfTime30-59DaysPastDueNotWorse":
                client.profile.number_of_times_30_59_days_late,
            "NumberOfTime60-89DaysPastDueNotWorse":
                client.profile.number_of_times_60_89_days_late,
            "NumberOfTimes90DaysLate":
                client.profile.number_of_times_90_more_days_late,
            "NumberRealEstateLoansOrLines":
                client_credits.count() * 0.2,
            "NumberOfOpenCreditLinesAndLoans":
                client_credits.count()
        }
        try:
            scoring_host = environ.get("SCORING_HOST", 'scoring')
            scoring_port = environ.get("SCORING_PORT", 'scoring')
            url = 'http://{}:{}/api/credits/scoring/'.format(scoring_host, scoring_port)
            req = Request(
                url,
                data=json.dumps(scoring_data),
                headers={"Content-Type": "application/json"}
            )
            response = urlopen(req)
            return Response(data=json.loads(response.read()))
        except Exception as e:
            raise ValidationError("Error with connection to scoring service: {}".format(e))

    @detail_route(methods=['GET'])
    def statistics(self, request, *args, **kwargs):
        client = self.get_object()
        client_credits = Credit.objects.filter(client=client)
        client_deposits = Deposit.objects.filter(client=client)
        client_transactions = Transaction.objects.filter(client=client)

        statistics = {
            "credits": {
                "total_count": client_credits.count(),
                "states_count": {
                    str(status[0]): client_credits.filter(status=status[0]).count()
                    for status in Credit.STATUS_CHOICES
                }
            },
            "deposits": {
                "total_count": client_deposits.count(),
                "states_count": {
                    str(status[0]): client_deposits.filter(status=status[0]).count()
                    for status in Deposit.STATUS_CHOICES
                }
            },
            "transactions": {
                "total_count": client_transactions.count(),
                "states_count": {
                    str(type[0]): client_transactions.filter(type=type[0]).count()
                    for type in Transaction.TYPES
                }
            }
        }

        return Response(data=statistics)
