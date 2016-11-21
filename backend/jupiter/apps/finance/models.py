# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField, ArrayField
from finance.utils import money_field, percentage_field

class Product(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        permissions = (
            ('view_product', 'Can view product'),
        )

class Transaction(models.Model):
    # TODO: store the action?
    client = models.ForeignKey(settings.AUTH_USER_MODEL)
    product = models.ForeignKey(Product)
    info = models.CharField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        permissions = (
            ('view_transaction', 'Can view transaction'),
        )

class Contract(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL)
    product = models.ForeignKey(Product)
    signed_on = models.DateTimeField()

    class Meta:
        verbose_name = 'Contract'
        verbose_name_plural = 'Contracts'
        permissions = (
            ('view_contract', 'Can view contract'),
        )

class Account(Product):
    ACTIVE = 0
    CLOSED = 1
    DISABLED = 2
    STATUSES = [
        (ACTIVE, 'Active'),
        (CLOSED, 'Closed'),
        (DISABLED, 'Disabled'),
    ]

    # TODO: add terms?
    residue = money_field()
    status = models.IntegerField(choices=STATUSES, )

    class Meta:
        verbose_name = 'Checking account'
        verbose_name_plural = 'Checking accounts'
        permissions = (
            ('view_account', 'Can view account'),
        )


class DepositTemplate(models.Model):

    YEARLY = 0
    DAILY = 1
    MONTHLY = 2
    QUARTERLY = 3
    INDEXATIONS = [
        (YEARLY, 'Yearly'),
        (DAILY, 'Daily'),
        (MONTHLY, 'Monthly'),
        (QUARTERLY, 'Quarterly')
    ]

    ANYTIME = 0
    ANYTIME_WITH_LOSSY = 1
    ONLY_AFTER_END = 2

    CONCELLATION_CONDITIONS = [
        (ANYTIME, 'Anytime'),
        (ANYTIME_WITH_LOSSY, 'Anytime with lossy'),
        (ONLY_AFTER_END, 'Only after end of term'),
    ]

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True)
    percentage = JSONField() # here currency, duration and percents
    indexing = models.IntegerField(choices=INDEXATIONS, default=YEARLY)
    cancellation_condition = models.IntegerField(choices=CONCELLATION_CONDITIONS,default=ANYTIME_WITH_LOSSY)
    min_amount = money_field()
    max_amount = money_field()
    prolongation = models.BooleanField(default=False)
    additional_contributions = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'Deposit templates'
        verbose_name_plural = 'Deposit templates'
        permissions = (
            ('view_deposittemplate', 'Can view deposit template'),
        )

class Deposit(Product):
    ACTIVE = 0
    CLOSED = 1
    STATUSES = [
        (ACTIVE, 'Active'),
        (CLOSED, 'Closed'),
    ]

    amount = money_field()
    template = models.ForeignKey(DepositTemplate)
    status = models.IntegerField(choices=STATUSES)

    class Meta:
        verbose_name = 'Deposit'
        verbose_name_plural = 'Deposits'
        permissions = (
            ('view_deposit', 'Can view deposit'),
        )

class CreditTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True)
    annual_percentage_rate = percentage_field() #Our annual interest rate on the basis of its count the rest we need    min_amount = JSONField()
    max_amount = JSONField() #calculated as max(FIXED, SUM(ANNUAL_PERCENT*DURATION/12, PURCHASE_SUM*PURCHASE_MAX_PERCENT) )
    min_amount = JSONField() #calculated as max(FIXED, SUM(ANNUAL_PERCENT*DURATION/12, PURCHASE_SUM*PURCHASE_MIN_PERCENT) )
    max_duration = models.IntegerField(default=12) #in months
    fine_percentage = percentage_field()
    issue_online = models.BooleanField(default=False)
    allowed_methods_of_ensuring = ArrayField(models.IntegerField())
    # FINE = 0 #{неустойка}
    # PLEDGE = 1 #{залог}
    # SURETY = 2 #{поручительство}.

    class Meta:
        verbose_name = 'Credit templates'
        verbose_name_plural = 'Credit templates'
        permissions = (
            ('view_credittemplate', 'Can view credit template'),
        )

class Credit(Product):
    OPENED = 0
    FINED = 1
    PAID_OFF = 2
    CLOSED = 3
    STATUSES = [
        (OPENED, 'Opened'),
        (FINED, 'Fined'),
        (PAID_OFF, 'Paid off'),
        (CLOSED, 'Closed'),
    ]

    FINE = 0 #{неустойка}
    PLEDGE = 1 #{залог}, fine is also charged as long as you do not recognized as dodger, then confiscation
    SURETY = 2 #{поручительство}. fine is also charged as you long as do not recognized as dodger, then debts will be called from the guarantor
    ENSURINGS = [
        (FINE, "Fine"),
        (PLEDGE, "Plegde"),
        (SURETY, "Surety"),
    ]

    residue = money_field()
    current_penalty = money_field()
    next_payment_term = models.DateField()
    template = models.ForeignKey(CreditTemplate)
    status = models.IntegerField(choices=STATUSES)
    fine_percentage = percentage_field()
    method_of_ensuring = models.IntegerField(choices=ENSURINGS)


    class Meta:
        verbose_name = 'Credit'
        verbose_name_plural = 'Credits'
        permissions = (
            ('view_credit', 'Can view credit'),
        )