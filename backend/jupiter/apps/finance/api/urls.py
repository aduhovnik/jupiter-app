# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from finance.api.accounts.views import AccountView
from finance.api.contracts.views import ContractView
from finance.api.credits.views import CreditView, CreditTemplateView
from finance.api.deposits.views import DepositView, DepositTemplateView
from finance.api.transactions.views import TransactionView

router = DefaultRouter()
router.register('contracts', ContractView, base_name='contacts')
router.register('transactions', TransactionView, base_name='transactions')
router.register('accounts', AccountView, base_name='accounts')
router.register('deposits', DepositView, base_name='deposits')
router.register('deposits/templates', DepositTemplateView, base_name='deposit-templates')
router.register('credits', CreditView, base_name='credits')
router.register('credits/templates', CreditTemplateView, base_name='credit-templates')

urlpatterns = [
    url(r'^api/', include(router.urls))
]


